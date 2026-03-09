import { api, API_BASE, getTokens } from './client';
import type { FileResponse, FilePreview } from '$lib/types/api';

export function uploadFile(file: File) {
	const formData = new FormData();
	formData.append('file', file);
	return api<FileResponse>('/files/upload', {
		method: 'POST',
		body: formData,
	});
}

export function listFiles() {
	return api<FileResponse[]>('/files/');
}

export function getFilePreview(fileId: string) {
	return api<FilePreview>(`/files/${fileId}/preview`);
}

export function deleteFile(fileId: string) {
	return api<void>(`/files/${fileId}`, { method: 'DELETE' });
}
