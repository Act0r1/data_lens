<script lang="ts">
	const plans = [
		{
			name: 'Free', slug: 'free', price: '0 ₽', period: 'навсегда', pop: false,
			features: ['5 файлов/мес', '5 MB максимум', '10 сообщений/день', '3 анализа/мес'],
		},
		{
			name: 'Starter', slug: 'starter', price: '990 ₽', period: 'в месяц', pop: false,
			features: ['30 файлов/мес', '20 MB максимум', '50 сообщений/день', '15 анализов/мес'],
		},
		{
			name: 'Business', slug: 'business', price: '3 990 ₽', period: 'в месяц', pop: true,
			features: ['∞ файлов', '50 MB максимум', '∞ сообщений', '∞ анализов'],
		},
		{
			name: 'Pro', slug: 'pro', price: '9 990 ₽', period: 'в месяц', pop: false,
			features: ['∞ файлов', '100 MB максимум', 'API доступ', '∞ анализов'],
		},
	];
</script>

<section id="pricing" class="mx-auto max-w-[1100px] px-12 py-24">
	<div class="mb-2 text-xs font-medium text-accent">Тарифы</div>
	<h2 class="font-heading mb-12 text-4xl font-bold">Выберите план</h2>
	<div class="grid grid-cols-4 gap-4">
		{#each plans as plan}
			<div class="relative rounded-[var(--radius)] p-8 transition-all hover:-translate-y-1 {plan.pop ? 'bg-foreground text-primary-foreground border-transparent' : 'glass'}">
				{#if plan.pop}
					<div class="absolute -top-2.5 right-6 rounded-full bg-accent px-3 py-1 text-[0.7rem] font-semibold text-white">Популярный</div>
				{/if}
				<div class="mb-3 text-xs {plan.pop ? 'text-white/50' : 'text-muted-foreground'}">{plan.name}</div>
				<div class="font-heading mb-1 text-4xl font-bold">{plan.price}</div>
				<div class="mb-6 text-xs {plan.pop ? 'text-white/50' : 'text-muted-foreground'}">{plan.period}</div>
				<ul class="mb-6 list-none space-y-0 p-0">
					{#each plan.features as feat}
						<li class="border-b py-2 text-xs {plan.pop ? 'border-white/10 text-white/60' : 'border-[var(--glass-border)] text-muted-foreground'}">
							<span class="{plan.pop ? 'text-accent' : 'text-green'} font-bold">✓</span> {feat}
						</li>
					{/each}
				</ul>
				<a
					href="/register?plan={plan.slug}"
					class="block w-full rounded-xl px-4 py-3 text-center text-sm font-medium no-underline transition-all {plan.pop ? 'bg-white text-foreground' : 'border border-[var(--glass-border)] hover:border-foreground'}"
				>
					{plan.price === '0 ₽' ? 'Начать' : 'Выбрать'}
				</a>
			</div>
		{/each}
	</div>
</section>
