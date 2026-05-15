import type { AdminSnapshot, ChatResponse, ParentProfile, StudentProfile, SummaryResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function createProfile(parent: ParentProfile, student: StudentProfile) {
  return request('/api/profiles', {
    method: 'POST',
    body: JSON.stringify({ parent, student }),
  });
}

export async function sendChatMessage(params: {
  profileId?: number;
  sessionId?: string;
  student?: StudentProfile;
  message: string;
}): Promise<ChatResponse> {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      profile_id: params.profileId,
      session_id: params.sessionId,
      student: params.student,
      message: params.message,
    }),
  });
}

export async function joinWaitlist(payload: {
  parent_name: string;
  email: string;
  child_grade: '3' | '4' | '5' | 'not_sure';
  note?: string;
}) {
  return request<{ id: number; message: string }>('/api/waitlist', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getSessionSummary(sessionId: string): Promise<SummaryResponse> {
  return request(`/api/sessions/${sessionId}/summary`);
}

export async function getAdminSnapshot(): Promise<AdminSnapshot> {
  return request('/api/admin/snapshot');
}
