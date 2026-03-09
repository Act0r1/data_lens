<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<div class="relative z-[1] min-h-screen">
	{@render children()}
</div>
