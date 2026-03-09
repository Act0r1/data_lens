import { getChatHistory, sendMessage } from '$lib/api/chat';
import { USE_MOCK } from '$lib/mock/index';
import { mockChatHistory, mockStreamChunks } from '$lib/mock/chat';
import type { ChatMessageResponse } from '$lib/types/api';

let messages = $state<ChatMessageResponse[]>([]);
let streamingContent = $state('');
let isStreaming = $state(false);

function delay(ms: number) {
	return new Promise(r => setTimeout(r, ms));
}

export const chatStore = {
	get messages() { return messages; },
	get streamingContent() { return streamingContent; },
	get isStreaming() { return isStreaming; },

	async loadHistory(analysisId: string) {
		if (USE_MOCK) {
			messages = [...mockChatHistory];
			return;
		}
		messages = await getChatHistory(analysisId);
	},

	async send(analysisId: string, content: string) {
		const userMsg: ChatMessageResponse = {
			id: crypto.randomUUID(),
			role: 'user',
			content,
			chart_spec: null,
			created_at: new Date().toISOString(),
		};
		messages = [...messages, userMsg];
		streamingContent = '';
		isStreaming = true;

		try {
			if (USE_MOCK) {
				for (const chunk of mockStreamChunks) {
					await delay(50 + Math.random() * 50);
					streamingContent += chunk;
				}
			} else {
				for await (const chunk of sendMessage(analysisId, content)) {
					streamingContent += chunk;
				}
			}
			const assistantMsg: ChatMessageResponse = {
				id: crypto.randomUUID(),
				role: 'assistant',
				content: streamingContent,
				chart_spec: null,
				created_at: new Date().toISOString(),
			};
			messages = [...messages, assistantMsg];
		} finally {
			streamingContent = '';
			isStreaming = false;
		}
	},

	reset() {
		messages = [];
		streamingContent = '';
		isStreaming = false;
	},
};
