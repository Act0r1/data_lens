<script lang="ts">
	import { BarChart3, Store, Bot, LineChart, Zap, Shield } from 'lucide-svelte';

	const features = [
		{ icon: BarChart3, name: 'Умный парсинг', desc: 'CSV, Excel, любая кодировка. Определяем cp1251, разделители, типы данных автоматически.' },
		{ icon: Store, name: 'WB / Ozon / 1С', desc: 'Распознаём формат выгрузки и даём специализированные рекомендации по вашей нише.' },
		{ icon: Bot, name: 'AI-чат', desc: 'Задавайте вопросы по данным на русском языке. Мгновенные ответы с графиками.' },
		{ icon: LineChart, name: 'Автографики', desc: 'Интерактивные визуализации генерируются автоматически на основе найденных паттернов.' },
		{ icon: Zap, name: 'Аномалии и тренды', desc: 'Z-score, IQR, линейная регрессия, корреляции Пирсона — всё автоматически.' },
		{ icon: Shield, name: 'Безопасность', desc: 'Данные зашифрованы, хранятся в российских дата-центрах. Полный контроль доступа.' },
	];
</script>

<section id="features" class="mx-auto max-w-[1100px] px-12 py-24">
	<div class="mb-2 text-xs font-medium text-accent">Возможности</div>
	<h2 class="font-heading mb-12 max-w-[500px] text-4xl font-bold leading-tight">Всё для анализа данных вашего бизнеса</h2>
	<div class="grid grid-cols-3 gap-4">
		{#each features as feat}
			<div class="glass rounded-[var(--radius)] p-8 transition-all hover:-translate-y-1 hover:shadow-[var(--glass-shadow)]">
				<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-[14px] bg-accent-light">
					<feat.icon class="h-5 w-5 text-accent" />
				</div>
				<div class="mb-2 font-semibold">{feat.name}</div>
				<div class="text-sm leading-relaxed text-muted-foreground">{feat.desc}</div>
			</div>
		{/each}
	</div>
</section>
