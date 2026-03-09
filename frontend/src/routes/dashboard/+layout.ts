import { redirect } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';

export const ssr = false;

export const load: LayoutLoad = async () => {
	if (import.meta.env.VITE_USE_MOCK === 'true') return;
	const raw = localStorage.getItem('auth');
	if (!raw) throw redirect(302, '/login');
	try {
		const parsed = JSON.parse(raw);
		if (!parsed.access_token) throw redirect(302, '/login');
	} catch {
		throw redirect(302, '/login');
	}
};
