<script lang="ts">
	import InsightCard from './InsightCard.svelte';
	import type { InsightItem } from '$lib/types/api';

	let { insights }: { insights: InsightItem[] } = $props();
</script>

<div class="mb-4 grid grid-cols-2 gap-4">
	{#each insights as insight}
		<InsightCard {insight} />
	{/each}
</div>
