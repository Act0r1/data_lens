import type { AnalysisResponse } from '$lib/types/api';

export const mockAnalysis: AnalysisResponse = {
	id: 'an-001-mock-analysis-id',
	status: 'completed',
	title: 'wb_sales_jan_2025.xlsx',
	insights: [
		{
			type: 'trend',
			title: 'Рост выручки на 23% за квартал',
			description: 'Линейная регрессия: R² = 0.87, наклон = 12 400₽/день',
			severity: 'info',
			data: null,
		},
		{
			type: 'anomaly',
			title: 'Резкий рост возвратов 15-17 января',
			description: 'Z-score = 4.2, возвраты в 3x выше среднего',
			severity: 'warning',
			data: null,
		},
		{
			type: 'correlation',
			title: 'Скидка ↔ Объём продаж',
			description: 'Пирсон: 0.82. Больше скидка → больше продаж, но маржа падает',
			severity: 'info',
			data: null,
		},
		{
			type: 'business',
			title: '5 SKU генерируют 60% убытков',
			description: 'WB-4521, WB-4533, WB-4590 убыточны из-за логистики',
			severity: 'warning',
			data: null,
		},
	],
	chart_specs: [
		{
			$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
			title: { text: 'Выручка по дням' },
			width: 'container',
			height: 220,
			data: {
				values: [
					{ day: '01', revenue: 84000 }, { day: '02', revenue: 92000 },
					{ day: '03', revenue: 78000 }, { day: '04', revenue: 105000 },
					{ day: '05', revenue: 98000 }, { day: '06', revenue: 112000 },
					{ day: '07', revenue: 125000 }, { day: '08', revenue: 118000 },
					{ day: '09', revenue: 134000 }, { day: '10', revenue: 142000 },
					{ day: '11', revenue: 128000 }, { day: '12', revenue: 156000 },
					{ day: '13', revenue: 148000 }, { day: '14', revenue: 165000 },
				],
			},
			mark: { type: 'area', color: '#e8450e', opacity: 0.3, line: { color: '#e8450e', strokeWidth: 2 } },
			encoding: {
				x: { field: 'day', type: 'ordinal', title: 'День' },
				y: { field: 'revenue', type: 'quantitative', title: 'Выручка, ₽' },
			},
		},
		{
			$schema: 'https://vega.github.io/schema/vega-lite/v5.json',
			title: { text: 'Возвраты по категориям' },
			width: 'container',
			height: 220,
			data: {
				values: [
					{ category: 'Одежда', returns: 12.5 },
					{ category: 'Обувь', returns: 18.3 },
					{ category: 'Аксессуары', returns: 5.2 },
					{ category: 'Электроника', returns: 8.1 },
					{ category: 'Дом', returns: 3.4 },
				],
			},
			mark: { type: 'bar', color: '#2563eb', cornerRadiusEnd: 6 },
			encoding: {
				x: { field: 'category', type: 'nominal', title: 'Категория' },
				y: { field: 'returns', type: 'quantitative', title: 'Возвраты, %' },
			},
		},
	],
	llm_tokens_used: 4200,
	created_at: '2025-01-12T10:35:00Z',
	completed_at: '2025-01-12T10:36:30Z',
};
