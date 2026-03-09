const API_BASE = '/api/v1';

let refreshPromise: Promise<void> | null = null;

function getTokens() {
	const raw = localStorage.getItem('auth');
	if (!raw) return null;
	try {
		return JSON.parse(raw) as { access_token: string; refresh_token: string };
	} catch {
		return null;
	}
}

function setTokens(tokens: { access_token: string; refresh_token: string }) {
	const existing = localStorage.getItem('auth');
	const parsed = existing ? JSON.parse(existing) : {};
	localStorage.setItem('auth', JSON.stringify({ ...parsed, ...tokens }));
}

function clearTokens() {
	localStorage.removeItem('auth');
}

async function refreshToken(): Promise<void> {
	const tokens = getTokens();
	if (!tokens?.refresh_token) {
		clearTokens();
		throw new Error('No refresh token');
	}
	const res = await fetch(`${API_BASE}/auth/refresh`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ refresh_token: tokens.refresh_token }),
	});
	if (!res.ok) {
		clearTokens();
		throw new Error('Refresh failed');
	}
	const data = await res.json();
	setTokens(data);
}

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
	const tokens = getTokens();
	const headers = new Headers(options.headers);
	if (tokens?.access_token) {
		headers.set('Authorization', `Bearer ${tokens.access_token}`);
	}
	if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
		headers.set('Content-Type', 'application/json');
	}

	let res = await fetch(`${API_BASE}${path}`, { ...options, headers });

	if (res.status === 401 && tokens?.refresh_token) {
		if (!refreshPromise) {
			refreshPromise = refreshToken().finally(() => { refreshPromise = null; });
		}
		await refreshPromise;

		const newTokens = getTokens();
		if (newTokens?.access_token) {
			headers.set('Authorization', `Bearer ${newTokens.access_token}`);
		}
		res = await fetch(`${API_BASE}${path}`, { ...options, headers });
	}

	if (res.status === 204) return undefined as T;

	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'Request failed' }));
		throw new Error(error.detail || `HTTP ${res.status}`);
	}

	return res.json();
}

export { getTokens, setTokens, clearTokens, API_BASE };
