<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import UploadZone from '$lib/components/dashboard/UploadZone.svelte';
	import FileTable from '$lib/components/dashboard/FileTable.svelte';
	import { filesStore } from '$lib/stores/files.svelte';

	let pollInterval: ReturnType<typeof setInterval>;

	onMount(() => {
		filesStore.load();
		pollInterval = setInterval(() => {
			const hasProcessing = filesStore.files.some(f => f.status === 'processing' || f.status === 'uploaded');
			if (hasProcessing) filesStore.load();
		}, 3000);
		return () => clearInterval(pollInterval);
	});
</script>

<div class="mb-6 flex items-center justify-between">
	<div>
		<h1 class="font-heading text-2xl font-bold">Мои файлы</h1>
		<p class="text-sm text-muted-foreground">Загрузите данные для анализа</p>
	</div>
</div>

<UploadZone />
<FileTable />
