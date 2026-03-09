import { getAnalysis } from '$lib/api/analysis';
import { getChartSpecs } from '$lib/api/charts';
import { USE_MOCK } from '$lib/mock/index';
import { mockAnalysis } from '$lib/mock/analysis';
import type { AnalysisResponse } from '$lib/types/api';

let current = $state<AnalysisResponse | null>(null);
let chartSpecs = $state<Record<string, unknown>[]>([]);
let loading = $state(false);

export const analysisStore = {
	get current() { return current; },
	get chartSpecs() { return chartSpecs; },
	get loading() { return loading; },

	async load(id: string) {
		loading = true;
		try {
			if (USE_MOCK) {
				current = { ...mockAnalysis, id };
				chartSpecs = mockAnalysis.chart_specs || [];
				return;
			}
			current = await getAnalysis(id);
			if (current.chart_specs) {
				chartSpecs = current.chart_specs;
			} else {
				chartSpecs = await getChartSpecs(id);
			}
		} finally {
			loading = false;
		}
	},

	reset() {
		current = null;
		chartSpecs = [];
	},
};
