<script lang="ts">
	import { marked } from 'marked';
	import DOMPurify from 'dompurify';
	import type { ChatMessageResponse } from '$lib/types/api';

	let { message }: { message: ChatMessageResponse } = $props();

	const html = $derived(
		message.role === 'assistant'
			? DOMPurify.sanitize(marked.parse(message.content) as string)
			: ''
	);
</script>

<div class="max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed
	{message.role === 'user'
		? 'self-end rounded-br-sm bg-foreground text-primary-foreground'
		: 'self-start rounded-bl-sm bg-white/70 text-foreground'}">
	{#if message.role === 'assistant'}
		<div class="prose prose-sm max-w-none [&_p]:mb-2 [&_p:last-child]:mb-0 [&_ol]:pl-4 [&_ul]:pl-4 [&_li]:mb-1">
			{@html html}
		</div>
	{:else}
		{message.content}
	{/if}
</div>
