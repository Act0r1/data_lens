<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import Logo from '$lib/components/shared/Logo.svelte';
	import { auth } from '$lib/stores/auth.svelte';
	import { Files, BarChart3, CreditCard, Settings, LogOut } from 'lucide-svelte';

	const items = [
		{ icon: Files, label: 'Файлы', href: '/dashboard' },
		{ icon: BarChart3, label: 'Анализы', href: '/dashboard/analyses' },
		{ icon: CreditCard, label: 'Тарифы', href: '/dashboard/billing' },
		{ icon: Settings, label: 'Настройки', href: '/dashboard/settings' },
	];

	function handleLogout() {
		auth.logout();
		goto('/login');
	}
</script>

<aside class="glass sticky top-6 h-fit rounded-[var(--radius)] py-6">
	<div class="mb-6 px-6">
		<a href="/dashboard" class="no-underline"><Logo size="md" /></a>
	</div>

	<nav class="space-y-0.5">
		{#each items as item}
			{@const active = page.url.pathname === item.href || (item.href !== '/dashboard' && page.url.pathname.startsWith(item.href))}
			<a
				href={item.href}
				class="flex items-center gap-3 px-6 py-2.5 text-sm transition-all no-underline
					{active ? 'border-r-2 border-accent bg-accent/5 font-medium text-foreground' : 'text-muted-foreground hover:bg-black/[0.02] hover:text-foreground'}"
			>
				<item.icon class="h-4 w-4" />
				{item.label}
			</a>
		{/each}
	</nav>

	<div class="mt-8 px-4">
		<button
			onclick={handleLogout}
			class="flex w-full items-center gap-3 rounded-xl px-2 py-2.5 text-sm text-muted-foreground transition-all hover:bg-black/[0.02] hover:text-foreground"
		>
			<LogOut class="h-4 w-4" />
			Выход
		</button>
	</div>
</aside>
