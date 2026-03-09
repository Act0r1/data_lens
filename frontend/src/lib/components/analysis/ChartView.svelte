<script lang="ts">
	import { onMount } from 'svelte';

	let { spec, title = '' }: { spec: Record<string, unknown>; title?: string } = $props();

	let container: HTMLDivElement;

	onMount(async () => {
		const vegaEmbed = (await import('vega-embed')).default;
		const patchedSpec = {
			...spec,
			background: 'transparent',
			config: {
				...(spec.config as Record<string, unknown> || {}),
				font: 'DM Sans',
				axis: { labelFont: 'DM Sans', titleFont: 'DM Sans' },
				legend: { labelFont: 'DM Sans', titleFont: 'DM Sans' },
			},
		};
		await vegaEmbed(container, patchedSpec as any, {
			actions: false,
			renderer: 'svg',
		});
	});
</script>

<div class="glass rounded-[var(--radius)] p-6">
	{#if title}
		<div class="mb-4 text-xs font-medium text-muted-foreground">{title}</div>
	{/if}
	<div bind:this={container} class="min-h-[220px]"></div>
</div>
