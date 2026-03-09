<script lang="ts">
	import { Upload } from 'lucide-svelte';
	import { filesStore } from '$lib/stores/files.svelte';

	let dragover = $state(false);
	let fileInput: HTMLInputElement;

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		dragover = false;
		const file = e.dataTransfer?.files[0];
		if (file) filesStore.upload(file);
	}

	function handleSelect(e: Event) {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];
		if (file) filesStore.upload(file);
		input.value = '';
	}
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
	class="glass mb-6 cursor-pointer rounded-[var(--radius)] border-2 border-dashed border-black/10 p-12 text-center transition-all
		{dragover ? 'border-accent bg-accent-light' : 'hover:border-accent hover:bg-accent-light'}"
	ondragover={(e) => { e.preventDefault(); dragover = true; }}
	ondragleave={() => dragover = false}
	ondrop={handleDrop}
	onclick={() => fileInput.click()}
	onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') fileInput.click(); }}
	role="button"
	tabindex="0"
>
	<div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-accent-light">
		<Upload class="h-5 w-5 text-accent" />
	</div>
	<div class="font-semibold">Перетащите файл сюда</div>
	<div class="mt-1 text-xs text-muted-foreground">CSV, TSV, Excel — до 50 MB</div>
	<input bind:this={fileInput} type="file" accept=".csv,.tsv,.xlsx,.xls" onchange={handleSelect} class="hidden" />
</div>
