<script lang="ts">
	let { status }: { status: string } = $props();

	const config: Record<string, { label: string; class: string }> = {
		ready: { label: '● Готов', class: 'bg-green/10 text-green' },
		processing: { label: '◌ Обработка', class: 'bg-blue/10 text-blue animate-pulse' },
		uploaded: { label: '◌ Загружен', class: 'bg-blue/10 text-blue' },
		error: { label: '✕ Ошибка', class: 'bg-accent/10 text-accent' },
		pending: { label: '◌ Ожидание', class: 'bg-muted-foreground/10 text-muted-foreground' },
	};

	const c = $derived(config[status] || config.pending);
</script>

<span class="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium {c.class}">
	{c.label}
</span>
