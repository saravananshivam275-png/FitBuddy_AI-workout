import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


def generate_workout_plan(goal: str, fitness_level: str, days_per_week: int) -> str:
    """Create a simple AI-generated workout plan using Gemini or a demo fallback."""
    goal = (goal or "general fitness").strip()
    fitness_level = (fitness_level or "beginner").strip()
    days_per_week = int(days_per_week or 3)

    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    api_key = os.getenv("GEMINI_API_KEY")

    if demo_mode or not api_key or genai is None:
        return (
            f"Sample Workout Plan\n"
            f"Goal: {goal}\n"
            f"Fitness level: {fitness_level}\n"
            f"Training days: {days_per_week}\n\n"
            "- Day 1: Upper body strength workout (45 min)\n"
            "- Day 2: Lower body strength workout (45 min)\n"
            "- Day 3: Cardio and core (30-40 min)\n"
            "- Day 4: Recovery walk + mobility (20-30 min)\n"
            "- Day 5: Full-body conditioning (40 min)\n"
            "- Day 6: Rest day\n"
            "- Day 7: Optional active recovery"
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash"))

    prompt = (
        f"Create a clear and motivating {fitness_level}-level workout plan for {goal}. "
        f"The user trains {days_per_week} days per week. "
        "Include warm-up, main workout, sets, reps, and rest times. "
        "Keep it practical and safe."
    )

    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, "text") and response.text else "Workout plan is unavailable right now."
