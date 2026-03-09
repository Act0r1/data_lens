<script lang="ts">
	import type { InsightItem } from '$lib/types/api';

	let { insight }: { insight: InsightItem } = $props();

	const tagColors: Record<string, string> = {
		trend: 'bg-blue/10 text-blue',
		anomaly: 'bg-accent/10 text-accent',
		correlation: 'bg-green/10 text-green',
		business: 'bg-accent/10 text-accent',
	};

	const tagLabels: Record<string, string> = {
		trend: 'Тренд',
		anomaly: 'Аномалия',
		correlation: 'Корреляция',
		business: 'Бизнес',
	};

	const sevColors: Record<string, string> = {
		warning: 'text-accent border-accent/30',
		info: 'text-blue border-blue/30',
		critical: 'text-accent border-accent/50',
	};
</script>

<div class="glass rounded-[var(--radius)] p-6 transition-transform hover:-translate-y-0.5">
	<div class="mb-3 flex items-center justify-between">
		<span class="rounded-full px-2.5 py-0.5 text-[0.7rem] font-semibold {tagColors[insight.type] || tagColors.trend}">
			{tagLabels[insight.type] || insight.type}
		</span>
		<span class="rounded-full border px-2 py-0.5 text-[0.65rem] font-medium {sevColors[insight.severity] || sevColors.info}">
			{insight.severity}
		</span>
	</div>
	<div class="mb-1.5 text-sm font-semibold">{insight.title}</div>
	<div class="text-xs leading-relaxed text-muted-foreground">{insight.description}</div>
</div>
