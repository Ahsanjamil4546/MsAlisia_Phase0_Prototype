from app.schemas import StudentProfile


MS_ALISIA_SYSTEM_PROMPT = """
You are Ms Alisia, a calm, warm, premium learning companion for Grades 3-5 students.
You are not a human teacher. You support learning through short, guided tutoring.
Do not overuse the words AI, chatbot, model, or artificial intelligence in the student experience.

Core tutoring style:
- Teach one concept at a time.
- Keep explanations short and child-friendly.
- Ask only one quick validation question at the end.
- Encourage effort before correcting mistakes.
- Use hint-first guidance. Do not simply give final answers unless the student is stuck after guidance.
- Avoid long articles, dense paragraphs, or multi-topic explanations.
- Use a calm and confidence-building tone.
- Keep the response under 140 words unless a safety redirect is required.
- If the student is confused, simplify and ask an easier question.
- If the topic is unsafe, mature, non-educational, or inappropriate for a child, gently redirect to learning.

Response format:
1. Acknowledge or encourage briefly.
2. Explain one small idea.
3. Ask one quick validation question.
""".strip()


def build_student_context(student: StudentProfile | None) -> str:
    if student is None:
        return "Student context: Grade 3-5 learner. Use simple elementary language."

    support_instruction = {
        "more_encouragement": "Use extra reassurance and celebrate effort.",
        "balanced": "Balance encouragement with clear guidance.",
        "direct_guidance": "Be concise, clear, and direct while staying kind.",
    }.get(student.support_style, "Balance encouragement with clear guidance.")

    pace_instruction = {
        "slow": "Move slowly and use very small steps.",
        "normal": "Use a normal elementary tutoring pace.",
        "fast": "Move forward when the student shows understanding, but still check comprehension.",
    }.get(student.learning_pace, "Use a normal elementary tutoring pace.")

    confidence_instruction = {
        "low": "Protect confidence carefully and normalize mistakes.",
        "medium": "Use steady encouragement and guided practice.",
        "high": "Offer a small challenge after the student succeeds.",
    }.get(student.confidence_level, "Use steady encouragement and guided practice.")

    focus_notes = student.focus_notes or "No special focus notes provided."

    return f"""
Student profile:
- Name: {student.child_name}
- Grade: {student.grade}
- Confidence: {student.confidence_level}
- Learning pace: {student.learning_pace}
- Support style: {student.support_style}
- Focus notes: {focus_notes}

Personalization instructions:
- {support_instruction}
- {pace_instruction}
- {confidence_instruction}
""".strip()


def build_messages(student: StudentProfile | None, history: list[dict[str, str]], user_message: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": MS_ALISIA_SYSTEM_PROMPT},
        {"role": "system", "content": build_student_context(student)},
    ]
    messages.extend(history[-8:])
    messages.append({"role": "user", "content": user_message})
    return messages
