export type Grade = '3' | '4' | '5';
export type ConfidenceLevel = 'low' | 'medium' | 'high';
export type LearningPace = 'slow' | 'normal' | 'fast';
export type SupportStyle = 'more_encouragement' | 'balanced' | 'direct_guidance';

export interface ParentProfile {
  parent_name: string;
  email: string;
}

export interface StudentProfile {
  child_name: string;
  grade: Grade;
  confidence_level: ConfidenceLevel;
  learning_pace: LearningPace;
  support_style: SupportStyle;
  focus_notes?: string;
}

export interface ProfileResponse {
  profile_id: number;
  parent: ParentProfile;
  student: StudentProfile;
  created_at: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  session_id: string;
  reply: string;
  provider: 'groq' | 'demo';
  model: string;
  next_action?: string;
}

export interface SummaryResponse {
  session_id: string;
  total_turns: number;
  latest_topic: string;
  strengths: string[];
  needs_support: string[];
  recommended_next_step: string;
}

export interface AdminSnapshot {
  profiles: number;
  waitlist_signups: number;
  sessions: number;
  messages: number;
}
