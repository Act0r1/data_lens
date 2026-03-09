export interface UserRegister {
	email: string;
	password: string;
	name?: string;
}

export interface UserLogin {
	email: string;
	password: string;
}

export interface TokenResponse {
	access_token: string;
	refresh_token: string;
	token_type: string;
}

export interface RefreshRequest {
	refresh_token: string;
}

export interface UserResponse {
	id: string;
	email: string;
	name: string;
	plan_slug: string | null;
	created_at: string;
}

export interface FileResponse {
	id: string;
	original_name: string;
	mime_type: string;
	size_bytes: number;
	status: string;
	row_count: number | null;
	column_count: number | null;
	domain: string | null;
	created_at: string;
}

export interface FilePreview {
	columns: string[];
	rows: Record<string, unknown>[];
	total_rows: number;
}

export interface AnalysisCreate {
	file_ids: string[];
}

export interface InsightItem {
	type: string;
	title: string;
	description: string;
	severity: string;
	data: Record<string, unknown> | null;
}

export interface AnalysisResponse {
	id: string;
	status: string;
	title: string | null;
	insights: InsightItem[] | null;
	chart_specs: Record<string, unknown>[] | null;
	llm_tokens_used: number;
	created_at: string;
	completed_at: string | null;
}

export interface ChatMessageCreate {
	content: string;
}

export interface ChatMessageResponse {
	id: string;
	role: string;
	content: string;
	chart_spec: Record<string, unknown> | null;
	created_at: string;
}

export interface PlanResponse {
	id: string;
	slug: string;
	name: string;
	price_monthly: number;
	max_files_per_month: number;
	max_file_size_mb: number;
	max_chat_messages_per_day: number;
	max_analyses_per_month: number;
}

export interface UsageResponse {
	files_uploaded: number;
	analyses_run: number;
	chat_messages_sent: number;
	tokens_consumed: number;
}
