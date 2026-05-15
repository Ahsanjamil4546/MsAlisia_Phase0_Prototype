from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime


class StudentProfile(BaseModel):
    child_name: str = Field(..., min_length=1, max_length=50)
    grade: Literal["3", "4", "5"]
    confidence_level: Literal["low", "medium", "high"] = "medium"
    learning_pace: Literal["slow", "normal", "fast"] = "normal"
    support_style: Literal["more_encouragement", "balanced", "direct_guidance"] = "balanced"
    focus_notes: str | None = Field(default=None, max_length=500)


class ParentProfile(BaseModel):
    parent_name: str = Field(..., min_length=1, max_length=80)
    email: EmailStr


class ProfileRequest(BaseModel):
    parent: ParentProfile
    student: StudentProfile


class ProfileResponse(BaseModel):
    profile_id: int
    parent: ParentProfile
    student: StudentProfile
    created_at: datetime


class ChatRequest(BaseModel):
    profile_id: int | None = None
    session_id: str | None = None
    student: StudentProfile | None = None
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    provider: Literal["groq", "demo"]
    model: str
    next_action: str | None = None


class WaitlistRequest(BaseModel):
    parent_name: str = Field(..., min_length=1, max_length=80)
    email: EmailStr
    child_grade: Literal["3", "4", "5", "not_sure"] = "not_sure"
    note: str | None = Field(default=None, max_length=500)


class WaitlistResponse(BaseModel):
    id: int
    message: str


class SummaryResponse(BaseModel):
    session_id: str
    total_turns: int
    latest_topic: str
    strengths: list[str]
    needs_support: list[str]
    recommended_next_step: str


class AdminSnapshot(BaseModel):
    profiles: int
    waitlist_signups: int
    sessions: int
    messages: int
