import { api } from './client';
import type { UserRegister, UserLogin, TokenResponse, UserResponse } from '$lib/types/api';

export function register(data: UserRegister) {
	return api<UserResponse>('/auth/register', {
		method: 'POST',
		body: JSON.stringify(data),
	});
}

export function login(data: UserLogin) {
	return api<TokenResponse>('/auth/login', {
		method: 'POST',
		body: JSON.stringify(data),
	});
}

export function getMe() {
	return api<UserResponse>('/auth/me');
}
