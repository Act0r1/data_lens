<script lang="ts">
	import { Send } from 'lucide-svelte';

	let { onSend, disabled = false }: { onSend: (content: string) => void; disabled?: boolean } = $props();

	let value = $state('');

	function handleSubmit() {
		const text = value.trim();
		if (!text || disabled) return;
		onSend(text);
		value = '';
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSubmit();
		}
	}
</script>

<div class="flex gap-2 border-t border-[var(--glass-border)] px-6 py-4">
	<input
		bind:value
		onkeydown={handleKeydown}
		placeholder="Задайте вопрос..."
		{disabled}
		class="flex-1 rounded-xl border border-[var(--glass-border)] bg-white/60 px-4 py-2.5 text-sm text-foreground outline-none placeholder:text-muted-foreground focus:border-accent disabled:opacity-50"
	/>
	<button
		onclick={handleSubmit}
		{disabled}
		class="flex h-10 w-10 items-center justify-center rounded-xl bg-accent text-white transition-transform hover:scale-105 disabled:opacity-50"
	>
		<Send class="h-4 w-4" />
	</button>
</div>
