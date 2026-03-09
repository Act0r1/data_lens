<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import type { AnalysisResponse } from '$lib/types/api';

	let { analysis }: { analysis: AnalysisResponse } = $props();
</script>

<div class="glass flex items-center justify-between rounded-[var(--radius)] px-8 py-6 mb-4">
	<div>
		<h1 class="font-heading text-xl font-semibold">{analysis.title || 'Анализ'}</h1>
		<div class="mt-1 text-xs text-muted-foreground">
			{#if analysis.insights}
				{analysis.insights.length} инсайтов
			{/if}
		</div>
	</div>
	<div class="flex gap-2">
		<Button variant="outline" class="rounded-xl border-[var(--glass-border)] bg-[var(--surface)] backdrop-blur-xl">Экспорт</Button>
		<Button class="rounded-xl bg-foreground text-primary-foreground">Новый анализ</Button>
	</div>
</div>
