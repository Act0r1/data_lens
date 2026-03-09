<script lang="ts">
	import { cn } from '$lib/utils';

	let { class: className = '', children }: { class?: string; children?: any } = $props();
</script>

<div class={cn('glass rounded-[var(--radius)]', className)}>
	{@render children?.()}
</div>
