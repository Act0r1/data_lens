import { getMe } from '$lib/api/auth';
import { setTokens, clearTokens } from '$lib/api/client';
import { USE_MOCK } from '$lib/mock/index';
import type { UserResponse, TokenResponse } from '$lib/types/api';

let user = $state<UserResponse | null>(null);
let loading = $state(true);

export const auth = {
	get user() { return user; },
	get loading() { return loading; },
	get isAuthenticated() { return !!user; },

	async init() {
		if (USE_MOCK) {
			user = {
				id: 'mock-user-id',
				email: 'demo@datalens.ru',
				name: 'Демо пользователь',
				plan_slug: 'free',
				created_at: '2025-01-01T00:00:00Z',
			};
			loading = false;
			return;
		}
		const raw = localStorage.getItem('auth');
		if (!raw) {
			loading = false;
			return;
		}
		try {
			user = await getMe();
		} catch {
			clearTokens();
		}
		loading = false;
	},

	setSession(tokens: TokenResponse, userData: UserResponse) {
		setTokens(tokens);
		user = userData;
	},

	logout() {
		clearTokens();
		user = null;
	},
};
