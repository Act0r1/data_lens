import { api } from './client';
import type { AnalysisCreate, AnalysisResponse } from '$lib/types/api';

export function runAnalysis(data: AnalysisCreate) {
	return api<AnalysisResponse>('/analysis/run', {
		method: 'POST',
		body: JSON.stringify(data),
	});
}

export function listAnalyses() {
	return api<AnalysisResponse[]>('/analysis/');
}

export function getAnalysis(id: string) {
	return api<AnalysisResponse>(`/analysis/${id}`);
}
