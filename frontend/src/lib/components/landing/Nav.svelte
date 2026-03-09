<script lang="ts">
	import Logo from '$lib/components/shared/Logo.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Menu, X } from 'lucide-svelte';

	let open = $state(false);
</script>

<nav class="fixed top-4 left-1/2 z-50 flex -translate-x-1/2 items-center gap-8 rounded-full border border-[var(--glass-border)] bg-[var(--glass)] px-6 py-3 shadow-[var(--glass-shadow)] backdrop-blur-[24px] backdrop-saturate-[180%]">
	<a href="/" class="no-underline">
		<Logo size="md" />
	</a>
	<div class="hidden gap-1 md:flex">
		<a href="#features" class="rounded-full px-3.5 py-1.5 text-sm font-medium text-muted-foreground transition-all hover:bg-black/[0.04] hover:text-foreground no-underline">Возможности</a>
		<a href="#pricing" class="rounded-full px-3.5 py-1.5 text-sm font-medium text-muted-foreground transition-all hover:bg-black/[0.04] hover:text-foreground no-underline">Тарифы</a>
	</div>
	<a href="/login" class="hidden no-underline md:block">
		<Button class="rounded-full bg-accent px-5 text-sm font-medium text-white hover:bg-accent/90">
			Начать →
		</Button>
	</a>
	<button
		onclick={() => open = !open}
		class="flex h-8 w-8 items-center justify-center rounded-full text-foreground transition-colors hover:bg-black/[0.04] md:hidden"
	>
		{#if open}<X class="h-4 w-4" />{:else}<Menu class="h-4 w-4" />{/if}
	</button>
</nav>

{#if open}
	<button
		type="button"
		aria-label="Close menu"
		class="fixed inset-0 z-40 cursor-default border-0 bg-transparent p-0"
		onclick={() => open = false}
	></button>
	<div class="fixed top-20 left-1/2 z-50 flex w-[calc(100%-2rem)] max-w-sm -translate-x-1/2 flex-col gap-2 rounded-[var(--radius)] border border-[var(--glass-border)] bg-[var(--glass)] p-4 shadow-[var(--glass-shadow)] backdrop-blur-[24px] backdrop-saturate-[180%] md:hidden">
		<a href="#features" onclick={() => open = false} class="rounded-xl px-4 py-2.5 text-sm font-medium text-foreground no-underline transition-colors hover:bg-black/[0.04]">Возможности</a>
		<a href="#pricing" onclick={() => open = false} class="rounded-xl px-4 py-2.5 text-sm font-medium text-foreground no-underline transition-colors hover:bg-black/[0.04]">Тарифы</a>
		<a href="/login" onclick={() => open = false} class="no-underline">
			<Button class="w-full rounded-xl bg-accent text-sm font-medium text-white hover:bg-accent/90">
				Начать →
			</Button>
		</a>
	</div>
{/if}
