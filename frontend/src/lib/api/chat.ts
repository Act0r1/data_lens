import { api, API_BASE, getTokens } from './client';
import type { ChatMessageResponse } from '$lib/types/api';

export function getChatHistory(analysisId: string) {
	return api<ChatMessageResponse[]>(`/chat/${analysisId}/history`);
}

export async function* sendMessage(analysisId: string, content: string): AsyncGenerator<string> {
	const tokens = getTokens();
	const res = await fetch(`${API_BASE}/chat/${analysisId}/message`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			...(tokens?.access_token ? { Authorization: `Bearer ${tokens.access_token}` } : {}),
		},
		body: JSON.stringify({ content }),
	});

	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'Request failed' }));
		throw new Error(error.detail || `HTTP ${res.status}`);
	}

	const reader = res.body!.getReader();
	const decoder = new TextDecoder();
	let buffer = '';

	while (true) {
		const { done, value } = await reader.read();
		if (done) break;

		buffer += decoder.decode(value, { stream: true });
		const lines = buffer.split('\n');
		buffer = lines.pop() || '';

		for (const line of lines) {
			if (!line.startsWith('data: ')) continue;
			const data = line.slice(6).trim();
			if (data === '[DONE]') return;
			try {
				const parsed = JSON.parse(data);
				if (parsed.content) yield parsed.content;
			} catch {}
		}
	}
}
