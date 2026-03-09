import { listFiles, uploadFile, deleteFile } from '$lib/api/files';
import { USE_MOCK } from '$lib/mock/index';
import { mockFiles } from '$lib/mock/files';
import type { FileResponse } from '$lib/types/api';

let files = $state<FileResponse[]>([]);
let uploading = $state(false);

export const filesStore = {
	get files() { return files; },
	get uploading() { return uploading; },

	async load() {
		if (USE_MOCK) {
			files = [...mockFiles];
			return;
		}
		files = await listFiles();
	},

	async upload(file: File) {
		uploading = true;
		try {
			if (USE_MOCK) {
				const mock: FileResponse = {
					id: crypto.randomUUID(),
					original_name: file.name,
					mime_type: file.type,
					size_bytes: file.size,
					status: 'processing',
					row_count: null,
					column_count: null,
					domain: null,
					created_at: new Date().toISOString(),
				};
				files = [mock, ...files];
				return mock;
			}
			const res = await uploadFile(file);
			files = [res, ...files];
			return res;
		} finally {
			uploading = false;
		}
	},

	async remove(id: string) {
		if (!USE_MOCK) await deleteFile(id);
		files = files.filter(f => f.id !== id);
	},

	updateFile(id: string, updates: Partial<FileResponse>) {
		files = files.map(f => f.id === id ? { ...f, ...updates } : f);
	},
};
