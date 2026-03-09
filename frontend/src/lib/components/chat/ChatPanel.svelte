<script lang="ts">
	import { onMount } from 'svelte';
	import ChatMessage from './ChatMessage.svelte';
	import ChatInput from './ChatInput.svelte';
	import TypingIndicator from './TypingIndicator.svelte';
	import { chatStore } from '$lib/stores/chat.svelte';

	let { analysisId }: { analysisId: string } = $props();

	let chatBody: HTMLDivElement;
	let shouldAutoScroll = $state(true);

	onMount(() => {
		chatStore.loadHistory(analysisId);
	});

	function handleScroll() {
		const el = chatBody;
		shouldAutoScroll = el.scrollHeight - el.scrollTop - el.clientHeight < 100;
	}

	$effect(() => {
		// trigger on messages or streaming content change
		chatStore.messages;
		chatStore.streamingContent;
		if (shouldAutoScroll && chatBody) {
			chatBody.scrollTop = chatBody.scrollHeight;
		}
	});

	async function handleSend(content: string) {
		await chatStore.send(analysisId, content);
	}
</script>

<div class="sticky top-6 flex h-[calc(100vh-3rem)] flex-col overflow-hidden rounded-[var(--radius)] border border-[var(--glass-border)] bg-[var(--glass)] shadow-[var(--glass-shadow)] backdrop-blur-[24px] backdrop-saturate-[180%]">
	<div class="flex items-center gap-2 border-b border-[var(--glass-border)] px-6 py-4 text-sm font-semibold">
		<span class="h-2 w-2 rounded-full bg-green"></span>
		AI-чат по данным
	</div>

	<div bind:this={chatBody} onscroll={handleScroll} class="flex flex-1 flex-col gap-3 overflow-y-auto p-6">
		{#each chatStore.messages as msg}
			<ChatMessage message={msg} />
		{/each}
		{#if chatStore.isStreaming}
			<ChatMessage message={{ id: 'streaming', role: 'assistant', content: chatStore.streamingContent, chart_spec: null, created_at: '' }} />
		{/if}
		{#if chatStore.isStreaming && !chatStore.streamingContent}
			<TypingIndicator />
		{/if}
		{#if chatStore.messages.length === 0 && !chatStore.isStreaming}
			<div class="flex flex-1 items-center justify-center text-sm text-muted-foreground">
				Задайте вопрос по данным
			</div>
		{/if}
	</div>

	<ChatInput onSend={handleSend} disabled={chatStore.isStreaming} />
</div>
