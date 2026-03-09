import { api } from './client';

export function getChartSpecs(analysisId: string) {
	return api<Record<string, unknown>[]>(`/charts/${analysisId}/specs`);
}

export function generateChart(analysisId: string, prompt: string) {
	return api<Record<string, unknown>>(`/charts/${analysisId}/generate`, {
		method: 'POST',
		body: JSON.stringify({ prompt }),
	});
}
