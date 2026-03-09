<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import AnalysisHeader from '$lib/components/analysis/AnalysisHeader.svelte';
	import InsightsGrid from '$lib/components/analysis/InsightsGrid.svelte';
	import ChartView from '$lib/components/analysis/ChartView.svelte';
	import ChatPanel from '$lib/components/chat/ChatPanel.svelte';
	import { analysisStore } from '$lib/stores/analysis.svelte';
	import { chatStore } from '$lib/stores/chat.svelte';

	let { data } = $props();

	let pollInterval: ReturnType<typeof setInterval>;

	onMount(() => {
		analysisStore.load(data.analysisId);
		pollInterval = setInterval(() => {
			if (analysisStore.current?.status === 'pending' || analysisStore.current?.status === 'running') {
				analysisStore.load(data.analysisId);
			}
		}, 3000);
	});

	onDestroy(() => {
		clearInterval(pollInterval);
		analysisStore.reset();
		chatStore.reset();
	});
</script>

<div class="grid grid-cols-[1fr_380px] gap-4">
	<div class="min-w-0">
		{#if analysisStore.loading && !analysisStore.current}
			<Skeleton class="mb-4 h-24 rounded-[var(--radius)]" />
			<div class="mb-4 grid grid-cols-2 gap-4">
				<Skeleton class="h-40 rounded-[var(--radius)]" />
				<Skeleton class="h-40 rounded-[var(--radius)]" />
			</div>
			<Skeleton class="h-64 rounded-[var(--radius)]" />
		{:else if analysisStore.current}
			<AnalysisHeader analysis={analysisStore.current} />

			{#if analysisStore.current.status === 'pending' || analysisStore.current.status === 'running'}
				<div class="glass flex items-center justify-center rounded-[var(--radius)] py-20">
					<div class="text-center">
						<div class="mb-3 text-lg font-medium">Анализируем данные...</div>
						<div class="text-sm text-muted-foreground">Это может занять минуту</div>
					</div>
				</div>
			{:else}
				{#if analysisStore.current.insights?.length}
					<InsightsGrid insights={analysisStore.current.insights} />
				{/if}

				{#each analysisStore.chartSpecs as spec, i}
					<div class="mb-4">
						<ChartView {spec} title={(spec as any).title?.text || `График ${i + 1}`} />
					</div>
				{/each}
			{/if}
		{/if}
	</div>

	<ChatPanel analysisId={data.analysisId} />
</div>
