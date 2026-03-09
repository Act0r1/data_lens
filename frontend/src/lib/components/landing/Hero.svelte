<section class="flex min-h-screen flex-col items-center justify-center px-8 pt-24 pb-16 text-center">
	<div class="animate-fade-up mb-10 inline-flex items-center gap-2 rounded-full border border-[var(--glass-border)] bg-[var(--glass)] px-4 py-1.5 text-xs text-muted-foreground backdrop-blur-xl">
		<span class="animate-pulse-dot h-1.5 w-1.5 rounded-full bg-green"></span>
		AI-аналитика для российского бизнеса
	</div>

	<h1 class="animate-fade-up font-heading text-7xl font-black leading-[1.1] tracking-tight max-w-[700px] mb-6" style="animation-delay: 0.1s">
		Данные говорят.<br /><em class="font-light italic text-accent">Мы переводим.</em>
	</h1>

	<p class="animate-fade-up max-w-[500px] text-lg leading-relaxed text-muted-foreground mb-10" style="animation-delay: 0.2s">
		Загрузите CSV или Excel — AI найдёт аномалии, тренды и выбросы. Для селлеров WB, Ozon и малого бизнеса.
	</p>

	<div class="animate-fade-up flex gap-3" style="animation-delay: 0.3s">
		<a href="/register" class="inline-flex items-center rounded-[var(--radius)] bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all hover:-translate-y-0.5 hover:shadow-lg">
			Попробовать бесплатно
		</a>
		<button
			onclick={() => document.getElementById('demo-preview')?.scrollIntoView({ behavior: 'smooth' })}
			class="rounded-[var(--radius)] border border-[var(--glass-border)] bg-[var(--surface)] px-8 py-3.5 text-sm font-medium text-foreground backdrop-blur-xl transition-all hover:bg-white"
		>
			Смотреть демо
		</button>
	</div>

	<div id="demo-preview" class="animate-fade-up mt-16 w-full max-w-[900px] rounded-[var(--radius)] border border-[var(--glass-border)] bg-[var(--glass)] p-6 shadow-[var(--glass-shadow),0_0_0_1px_rgba(255,255,255,0.5)_inset] backdrop-blur-[24px] backdrop-saturate-[180%]" style="animation-delay: 0.4s">
		<div class="mb-5 flex items-center gap-2">
			<span class="h-2.5 w-2.5 rounded-full bg-[#ff5f57]"></span>
			<span class="h-2.5 w-2.5 rounded-full bg-[#febc2e]"></span>
			<span class="h-2.5 w-2.5 rounded-full bg-[#28c840]"></span>
		</div>
		<div class="grid grid-cols-3 gap-3">
			<div class="rounded-xl bg-white/50 p-5">
				<div class="mb-2 text-xs text-muted-foreground">Выручка</div>
				<div class="font-heading text-3xl font-semibold">2.4M ₽</div>
				<div class="mt-1 text-xs text-green">↑ 23.4%</div>
			</div>
			<div class="rounded-xl bg-white/50 p-5">
				<div class="mb-2 text-xs text-muted-foreground">Заказы</div>
				<div class="font-heading text-3xl font-semibold">1 847</div>
				<div class="mt-1 text-xs text-green">↑ 12.1%</div>
			</div>
			<div class="rounded-xl bg-white/50 p-5">
				<div class="mb-2 text-xs text-muted-foreground">Возвраты</div>
				<div class="font-heading text-3xl font-semibold">8.3%</div>
				<div class="mt-1 text-xs text-accent">↑ 2.1%</div>
			</div>
			<div class="col-span-3 h-40 overflow-hidden rounded-xl bg-white/50 p-5">
				<div class="flex h-full items-end gap-1 pt-8">
					{#each [35,12,55,18,42,8,68,22,50,15,75,20,60,10,85,25,70,14,90,28] as height, i}
						<div
							class="flex-1 rounded-t {i % 2 === 0 ? 'bg-accent' : 'bg-accent/25'}"
							style="height: {height}%; animation: barGrow 1s ease forwards; animation-delay: {0.1 + i * 0.02}s; opacity: 0; transform-origin: bottom;"
						></div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</section>
