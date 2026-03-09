<script lang="ts">
	import { page } from '$app/state';
	import Logo from '$lib/components/shared/Logo.svelte';
	import Sidebar from '$lib/components/dashboard/Sidebar.svelte';
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';

	let { children } = $props();

	onMount(() => {
		auth.init();
	});
</script>

<div class="grid min-h-screen grid-cols-[220px_1fr] gap-4 p-4 pt-6">
	<Sidebar />
	<main class="min-w-0">
		{@render children()}
	</main>
</div>
