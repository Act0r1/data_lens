export function formatBytes(bytes: number): string {
	if (bytes === 0) return '0 B';
	const k = 1024;
	const sizes = ['B', 'KB', 'MB', 'GB'];
	const i = Math.floor(Math.log(bytes) / Math.log(k));
	return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

export function formatDate(iso: string): string {
	const d = new Date(iso);
	return d.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' });
}

export function formatCurrency(amount: number): string {
	return new Intl.NumberFormat('ru-RU').format(amount) + ' ₽';
}

export function formatNumber(n: number): string {
	return new Intl.NumberFormat('ru-RU').format(n);
}
