from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import (
    add_waitlist,
    admin_snapshot,
    create_profile,
    get_profile,
    get_recent_history,
    init_db,
    store_message,
    summary_for_session,
)
from app.groq_client import GroqClientError, generate_with_llm
from app.schemas import (
    AdminSnapshot,
    ChatRequest,
    ChatResponse,
    ProfileRequest,
    ProfileResponse,
    SummaryResponse,
    WaitlistRequest,
    WaitlistResponse,
)
from app.tutor_prompt import NON_MATH_FALLBACK_RESPONSE, build_messages, is_math_only_request

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.post("/api/profiles", response_model=ProfileResponse)
def create_learning_profile(payload: ProfileRequest) -> ProfileResponse:
    saved = create_profile(payload.parent, payload.student)
    return ProfileResponse(**saved)


@app.get("/api/profiles/{profile_id}", response_model=ProfileResponse)
def read_learning_profile(profile_id: int) -> ProfileResponse:
    profile = get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(**profile)


@app.post("/api/waitlist", response_model=WaitlistResponse)
def join_waitlist(payload: WaitlistRequest) -> WaitlistResponse:
    item_id = add_waitlist(payload.parent_name, payload.email, payload.child_grade, payload.note)
    return WaitlistResponse(id=item_id, message="Thank you. We’ll notify you when MsAlisia is ready.")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    session_id = payload.session_id or str(uuid4())
    student = payload.student

    if payload.profile_id is not None:
        profile = get_profile(payload.profile_id)
        if profile:
            student = profile["student"]

    history = get_recent_history(session_id, limit=10)

    store_message(session_id, "user", payload.message, payload.profile_id)

    if not is_math_only_request(payload.message, history):
        store_message(session_id, "assistant", NON_MATH_FALLBACK_RESPONSE, payload.profile_id)
        return ChatResponse(
            session_id=session_id,
            reply=NON_MATH_FALLBACK_RESPONSE,
            provider="demo",
            model="math-only-guard",
            next_action="Ask the student to try a math-related question.",
        )

    messages = build_messages(student=student, history=history, user_message=payload.message)

    try:
        reply, provider, model = await generate_with_llm(messages)
    except GroqClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    store_message(session_id, "assistant", reply, payload.profile_id)

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        provider=provider,
        model=model,
        next_action="Ask the student to answer the quick validation question.",
    )


@app.get("/api/sessions/{session_id}/summary", response_model=SummaryResponse)
def read_session_summary(session_id: str) -> SummaryResponse:
    return SummaryResponse(**summary_for_session(session_id))


@app.get("/api/admin/snapshot", response_model=AdminSnapshot)
def read_admin_snapshot() -> AdminSnapshot:
    return AdminSnapshot(**admin_snapshot())
