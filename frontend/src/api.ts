import type { AdminSnapshot, ChatResponse, ParentProfile, ProfileResponse, StudentProfile, SummaryResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '');

function getApiBaseUrl(): string {
  if (!API_BASE_URL) {
    throw new Error('Missing VITE_API_BASE_URL. Add your Railway backend URL in the frontend environment variables.');
  }
  return API_BASE_URL;
}

function getErrorMessage(status: number, body: string): string {
  if (!body) return `Request failed with status ${status}`;

  try {
    const parsed = JSON.parse(body) as { detail?: unknown; message?: unknown };
    const detail = parsed.detail ?? parsed.message;
    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail)) return detail.map((item) => item.msg || JSON.stringify(item)).join(', ');
  } catch {
    // The API returned plain text or HTML. Use the raw body below.
  }

  return body;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${getApiBaseUrl()}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
      ...options,
    });
  } catch (error) {
    throw new Error(
      error instanceof TypeError
        ? 'Could not reach the backend API. Check VITE_API_BASE_URL and the backend CORS settings.'
        : 'Could not complete the request.',
    );
  }

  if (!response.ok) {
    const text = await response.text();
    throw new Error(getErrorMessage(response.status, text));
  }

  return response.json() as Promise<T>;
}

export async function createProfile(parent: ParentProfile, student: StudentProfile): Promise<ProfileResponse> {
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
