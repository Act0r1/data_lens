<script lang="ts">
	let { size = 'md' }: { size?: 'sm' | 'md' | 'lg' } = $props();

	const sizes = {
		sm: 'text-lg',
		md: 'text-xl',
		lg: 'text-2xl'
	};
</script>

<span class="font-heading font-black {sizes[size]}">
	Data<span class="text-accent">Lens</span>
</span>
