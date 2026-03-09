<script lang="ts">
	import { goto } from '$app/navigation';
	import { Trash2 } from 'lucide-svelte';
	import StatusPill from './StatusPill.svelte';
	import { filesStore } from '$lib/stores/files.svelte';
	import { runAnalysis } from '$lib/api/analysis';
	import { formatBytes, formatDate } from '$lib/utils/format';
	import type { FileResponse } from '$lib/types/api';

	async function handleClick(file: FileResponse) {
		if (file.status !== 'ready') return;
		const analysis = await runAnalysis({ file_ids: [file.id] });
		goto(`/dashboard/analysis/${analysis.id}`);
	}

	async function handleDelete(e: Event, id: string) {
		e.stopPropagation();
		filesStore.remove(id);
	}
</script>

<div class="glass overflow-hidden rounded-[var(--radius)]">
	<div class="grid grid-cols-[1fr_100px_100px_100px_50px] items-center border-b border-[var(--glass-border)] px-6 py-3 text-xs font-medium text-muted-foreground">
		<span>Файл</span><span>Размер</span><span>Статус</span><span>Дата</span><span></span>
	</div>
	{#each filesStore.files as file}
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<div
			class="grid cursor-pointer grid-cols-[1fr_100px_100px_100px_50px] items-center border-b border-[var(--glass-border)] px-6 py-3.5 text-sm transition-colors last:border-0 hover:bg-white/40"
			onclick={() => handleClick(file)}
			onkeydown={(e) => { if (e.key === 'Enter') handleClick(file); }}
			role="button"
			tabindex="0"
		>
			<span class="font-medium">{file.original_name}</span>
			<span class="text-muted-foreground">{formatBytes(file.size_bytes)}</span>
			<span><StatusPill status={file.status} /></span>
			<span class="text-muted-foreground">{formatDate(file.created_at)}</span>
			<button
				class="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition-all hover:bg-accent/10 hover:text-accent"
				onclick={(e) => handleDelete(e, file.id)}
			>
				<Trash2 class="h-4 w-4" />
			</button>
		</div>
	{/each}
	{#if filesStore.files.length === 0}
		<div class="px-6 py-12 text-center text-sm text-muted-foreground">
			Нет загруженных файлов
		</div>
	{/if}
</div>
