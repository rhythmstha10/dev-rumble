"""
Generates a day-by-day study plan. Doesn't need library data - it's the
"academic assistant" side of Campus AI - but still goes through Gemini
with a safe fallback so it never breaks without an API key.
"""
from ai_assistant.models import StudyPlanRequest
from ai_assistant.services import gemini_client

# A small set of generic topic buckets used only for the offline fallback,
# so a plan without Gemini still looks reasonable instead of just saying
# "Day 1: Study {subject}" every day.
_FALLBACK_FOCUS_AREAS = [
    "Fundamentals & key definitions",
    "Core concepts, part 1",
    "Core concepts, part 2",
    "Worked examples / practice problems",
    "Weak areas review",
    "Past papers / mock questions",
    "Final revision & summary sheet",
]


def _fallback_plan(subject: str, days: int, hours_per_day) -> str:
    lines = [f"Study plan for {subject} ({days} day(s), ~{hours_per_day}h/day):"]
    for day in range(1, days + 1):
        focus = _FALLBACK_FOCUS_AREAS[(day - 1) % len(_FALLBACK_FOCUS_AREAS)]
        lines.append(f"Day {day}: {focus}")
    lines.append(
        "Tip: spend the first 10 minutes of each session reviewing yesterday's notes before starting new material."
    )
    return "\n".join(lines)


def _build_prompt(subject: str, days: int, hours_per_day) -> str:
    return (
        "You are Campus AI, a study planning assistant. Create a concise day-by-day "
        f"study plan for the subject \"{subject}\", for a student with an exam in {days} "
        f"day(s), studying about {hours_per_day} hour(s) per day. "
        "Format as 'Day 1: ...', 'Day 2: ...' etc, each with 2-4 short bullet topics. "
        "Keep it realistic and specific to the subject. End with one short study tip."
    )


def generate_study_plan(user, subject: str, days: int, hours_per_day) -> dict:
    days = max(1, min(int(days), 30))

    used_ai = False
    try:
        plan_text = gemini_client.generate(_build_prompt(subject, days, hours_per_day))
        used_ai = True
    except gemini_client.GeminiUnavailableError:
        plan_text = _fallback_plan(subject, days, hours_per_day)

    StudyPlanRequest.objects.create(
        user=user,
        subject=subject,
        days_until_exam=days,
        hours_per_day=hours_per_day,
        plan_text=plan_text,
    )

    return {"plan": plan_text, "used_ai": used_ai}
