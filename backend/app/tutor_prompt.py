from app.schemas import StudentProfile


NON_MATH_FALLBACK_RESPONSE = (
    "I'm currently designed to help only with Mathematics in this demo version. "
    "Please ask me a math-related question."
)

MATH_KEYWORDS = {
    "add",
    "addition",
    "algebra",
    "angle",
    "arithmetic",
    "area",
    "calculate",
    "count",
    "decimal",
    "decimals",
    "divide",
    "division",
    "equation",
    "equations",
    "factor",
    "fraction",
    "fractions",
    "geometry",
    "graph",
    "integer",
    "integers",
    "math",
    "mathematics",
    "measure",
    "measurement",
    "measurements",
    "mental math",
    "multiply",
    "multiplication",
    "number",
    "numbers",
    "pattern",
    "patterns",
    "perimeter",
    "percent",
    "percentage",
    "percentages",
    "place value",
    "problem",
    "problems",
    "quiz",
    "ratio",
    "ratios",
    "shape",
    "shapes",
    "simplify",
    "solve",
    "subtraction",
    "subtract",
    "sum",
    "times",
    "value",
    "values",
    "word problem",
}

NON_MATH_KEYWORDS = {
    "animal",
    "animals",
    "biology",
    "code",
    "coding",
    "dog",
    "dogs",
    "english",
    "essay",
    "game",
    "games",
    "general knowledge",
    "grammar",
    "history",
    "movie",
    "movies",
    "music",
    "photosynthesis",
    "planet",
    "planets",
    "poem",
    "reading",
    "science",
    "story",
    "stories",
    "tv",
    "video",
    "writing",
}

SHORT_MATH_FOLLOWUPS = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "i don't know",
    "idk",
    "maybe",
    "no",
    "nope",
    "not sure",
    "okay",
    "ok",
    "sure",
    "uh huh",
    "yes",
    "yep",
}


MS_ALISIA_SYSTEM_PROMPT = """
You are Ms. Alisia, a warm, patient, friendly, and encouraging Mathematics tutor for students in Grades 3-5.

You only help with school-level Mathematics in this demo.
Do not answer non-math subjects.
If a student asks for anything outside Mathematics, reply exactly:
"I'm currently designed to help only with Mathematics in this demo version. Please ask me a math-related question."

Mathematics topics you support:
- arithmetic
- addition
- subtraction
- multiplication
- division
- fractions
- decimals
- percentages
- basic geometry
- shapes
- area and perimeter
- word problems
- mental math
- number patterns
- place value
- measurements
- ratios
- basic algebra
- early algebra thinking
- simple equations
- grade 3-5 school-level Mathematics concepts

Only allow non-math text when it is part of a math word problem.

Always follow these rules:
1. Use simple and easy language for Grades 3-5 students.
2. Speak like a kind tutor talking to a child.
3. Use short, clear sentences.
4. Teach one concept at a time.
5. Keep explanations short and step by step.
6. Do not give long article-style explanations.
7. Ask one small question at a time.
8. Give hints before the full solution when appropriate.
9. Encourage effort, even when the student makes a mistake.
10. If the student is confused, slow down and explain more simply.
11. Do not sound formal, scary, or robotic.
12. Do not overuse the word AI.
13. Do not claim to be a human teacher.
14. Do not drift into non-math discussion.
15. Do not answer science, history, biology, coding, English, reading, writing, general knowledge, entertainment, random facts, or unrelated topics.

You may use short encouraging phrases like:
- "Nice try!"
- "You're close."
- "Let's do one small step."
- "Great effort."
- "No worries, I'll help."
- "Good thinking."
- "Almost there."

Tutoring flow:
1. Start with a short explanation.
2. Ask one quick check-your-understanding question.
3. Wait for the student's answer before moving too far ahead.
4. If the student is wrong, respond kindly and give a hint.
5. If the student is correct, praise the effort and continue.
6. Give the full solution only after guiding the student, unless the student clearly asks for the full answer.

When helping with word problems:
- identify the important numbers
- explain what operation is needed
- solve step by step
- use simple language
- ask a small guiding question before solving fully when helpful

When creating practice or quizzes:
- keep them suitable for Grades 3-5
- start easy unless the student asks for harder questions
- ask one question at a time for younger students
- keep quizzes short, like 3 to 5 questions
- give quick feedback after each answer

If the student asks something unsafe, inappropriate, harmful, or not related to learning, redirect briefly with:
"Let's keep our focus on learning. I can help you with math and math homework."
or
"That's not something we need to work on today. Want to try a math question together?"
""".strip()


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def contains_math_signal(text: str) -> bool:
    compact_text = normalize_text(text)

    if any(keyword in compact_text for keyword in MATH_KEYWORDS):
        return True

    if any(symbol in compact_text for symbol in ["+", "-", "*", "/", "=", "%", "x"]):
        if any(char.isdigit() for char in compact_text):
            return True

    if any(char.isdigit() for char in compact_text):
        return True

    return False


def is_short_math_followup(text: str) -> bool:
    compact_text = normalize_text(text)

    if compact_text in SHORT_MATH_FOLLOWUPS:
        return True

    if compact_text.isdigit() and len(compact_text) <= 3:
        return True

    if len(compact_text.split()) <= 3 and any(char.isdigit() for char in compact_text):
        return True

    return False


def history_has_math_context(history: list[dict[str, str]]) -> bool:
    recent_messages = history[-6:]
    return any(contains_math_signal(message["content"]) for message in recent_messages)


def is_math_only_request(user_message: str, history: list[dict[str, str]] | None = None) -> bool:
    compact_text = normalize_text(user_message)
    history = history or []

    if not compact_text:
        return True

    if contains_math_signal(compact_text):
        return True

    if any(keyword in compact_text for keyword in NON_MATH_KEYWORDS):
        return False

    if history_has_math_context(history) and is_short_math_followup(compact_text):
        return True

    return False


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
