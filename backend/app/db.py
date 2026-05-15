import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from app.config import get_settings
from app.schemas import ParentProfile, StudentProfile


settings = get_settings()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_db_directory() -> None:
    db_path = Path(settings.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    ensure_db_directory()
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_json TEXT NOT NULL,
                student_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS waitlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_name TEXT NOT NULL,
                email TEXT NOT NULL,
                child_grade TEXT NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                profile_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def create_profile(parent: ParentProfile, student: StudentProfile) -> dict:
    created_at = utc_now()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO profiles (parent_json, student_json, created_at) VALUES (?, ?, ?)",
            (parent.model_dump_json(), student.model_dump_json(), created_at),
        )
        profile_id = int(cursor.lastrowid)
    return {"profile_id": profile_id, "parent": parent, "student": student, "created_at": created_at}


def get_profile(profile_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    if not row:
        return None
    return {
        "profile_id": row["id"],
        "parent": ParentProfile.model_validate_json(row["parent_json"]),
        "student": StudentProfile.model_validate_json(row["student_json"]),
        "created_at": row["created_at"],
    }


def add_waitlist(parent_name: str, email: str, child_grade: str, note: str | None) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO waitlist (parent_name, email, child_grade, note, created_at) VALUES (?, ?, ?, ?, ?)",
            (parent_name, email, child_grade, note, utc_now()),
        )
        return int(cursor.lastrowid)


def store_message(session_id: str, role: str, content: str, profile_id: int | None = None) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chat_messages (session_id, profile_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (session_id, profile_id, role, content, utc_now()),
        )


def get_recent_history(session_id: str, limit: int = 10) -> list[dict[str, str]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT role, content FROM chat_messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()
    messages = [{"role": row["role"], "content": row["content"]} for row in rows]
    return list(reversed(messages))


def admin_snapshot() -> dict:
    with get_connection() as conn:
        profiles = conn.execute("SELECT COUNT(*) AS c FROM profiles").fetchone()["c"]
        waitlist = conn.execute("SELECT COUNT(*) AS c FROM waitlist").fetchone()["c"]
        sessions = conn.execute("SELECT COUNT(DISTINCT session_id) AS c FROM chat_messages").fetchone()["c"]
        messages = conn.execute("SELECT COUNT(*) AS c FROM chat_messages").fetchone()["c"]
    return {"profiles": profiles, "waitlist_signups": waitlist, "sessions": sessions, "messages": messages}


def summary_for_session(session_id: str) -> dict:
    history = get_recent_history(session_id, limit=50)
    user_messages = [m["content"] for m in history if m["role"] == "user"]
    assistant_messages = [m["content"] for m in history if m["role"] == "assistant"]
    latest_topic = user_messages[-1][:80] if user_messages else "No topic yet"
    total_turns = len(user_messages)

    strengths = []
    needs_support = []

    all_text = " ".join(user_messages + assistant_messages).lower()
    if any(word in all_text for word in ["correct", "great", "nice", "well done"]):
        strengths.append("Participated in guided practice")
    else:
        strengths.append("Started the learning session")

    if any(word in all_text for word in ["fraction", "fractions"]):
        needs_support.append("Continue practicing fraction vocabulary and steps")
    elif any(word in all_text for word in ["multiplication", "multiply", "times"]):
        needs_support.append("Continue building multiplication fluency")
    elif any(word in all_text for word in ["division", "divide"]):
        needs_support.append("Continue practicing division reasoning")
    else:
        needs_support.append("Use one more quick practice question to confirm understanding")

    return {
        "session_id": session_id,
        "total_turns": total_turns,
        "latest_topic": latest_topic,
        "strengths": strengths,
        "needs_support": needs_support,
        "recommended_next_step": "Continue with one short guided practice activity.",
    }
