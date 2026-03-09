<script lang="ts">
	import { goto } from '$app/navigation';
	import Logo from '$lib/components/shared/Logo.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { register } from '$lib/api/auth';
	import { login } from '$lib/api/auth';
	import { auth } from '$lib/stores/auth.svelte';
	import { setTokens } from '$lib/api/client';
	import { getMe } from '$lib/api/auth';

	let name = $state('');
	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			await register({ email, password, name });
			const tokens = await login({ email, password });
			setTokens(tokens);
			const user = await getMe();
			auth.setSession(tokens, user);
			goto('/dashboard');
		} catch (err: any) {
			error = err.message || 'Ошибка регистрации';
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center px-4">
	<div class="glass w-full max-w-md rounded-[var(--radius)] p-8">
		<div class="mb-8 text-center">
			<Logo size="lg" />
			<p class="mt-2 text-sm text-muted-foreground">Создайте аккаунт</p>
		</div>

		<form onsubmit={handleSubmit} class="space-y-4">
			{#if error}
				<div class="rounded-xl bg-accent/10 px-4 py-3 text-sm text-accent">{error}</div>
			{/if}
			<div>
				<label for="name" class="mb-1.5 block text-sm font-medium">Имя</label>
				<Input id="name" bind:value={name} placeholder="Ваше имя" class="rounded-xl border-[var(--glass-border)] bg-white/60" />
			</div>
			<div>
				<label for="email" class="mb-1.5 block text-sm font-medium">Email</label>
				<Input id="email" type="email" bind:value={email} placeholder="you@company.ru" required class="rounded-xl border-[var(--glass-border)] bg-white/60" />
			</div>
			<div>
				<label for="password" class="mb-1.5 block text-sm font-medium">Пароль</label>
				<Input id="password" type="password" bind:value={password} placeholder="Минимум 6 символов" required class="rounded-xl border-[var(--glass-border)] bg-white/60" />
			</div>
			<Button type="submit" class="w-full rounded-xl bg-foreground text-primary-foreground hover:bg-foreground/90" disabled={loading}>
				{loading ? 'Создание...' : 'Создать аккаунт'}
			</Button>
		</form>

		<p class="mt-6 text-center text-sm text-muted-foreground">
			Уже есть аккаунт? <a href="/login" class="font-medium text-accent hover:underline">Войти</a>
		</p>
	</div>
</div>
