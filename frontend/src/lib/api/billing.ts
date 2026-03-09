import { api } from './client';
import type { PlanResponse, UsageResponse } from '$lib/types/api';

export function getPlans() {
	return api<PlanResponse[]>('/billing/plans');
}

export function getUsage() {
	return api<UsageResponse>('/billing/usage');
}

export function subscribe(planSlug: string) {
	return api<{ status: string; payment_url?: string }>(`/billing/subscribe?plan_slug=${planSlug}`, {
		method: 'POST',
	});
}
