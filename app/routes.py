from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.ai.init import generate_workout_plan


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# =========================================================
# HOME PAGE
# =========================================================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None,
            "nutrition": None,
            "feedback_result": None,
        },
    )


# =========================================================
# PERSONALIZED WORKOUT
# =========================================================

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,

    name: str = Form(""),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    fitness_level: str = Form(...),

    days_per_week: int = Form(...),

    intensity: str = Form(...),
):

    # Generate workout using your existing AI function
    result = generate_workout_plan(
        goal,
        fitness_level,
        days_per_week
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,

            "result": result,

            "nutrition": None,

            "feedback_result": None,

            "name": name,

            "age": age,

            "weight": weight,

            "goal": goal,

            "fitness_level": fitness_level,

            "days_per_week": days_per_week,

            "intensity": intensity,
        },
    )


# =========================================================
# NUTRITION TIPS
# =========================================================

@router.get("/nutrition", response_class=HTMLResponse)
async def nutrition(request: Request):

    nutrition_result = """
🥗 FITBUDDY AI - NUTRITION & RECOVERY TIPS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍎 DAILY NUTRITION

• Eat a balanced variety of vegetables and fruits.

• Include protein-rich foods such as eggs, fish,
  chicken, milk, yogurt, beans and lentils.

• Choose whole grains and other nutritious
  carbohydrate sources.

• Drink water regularly throughout the day.

• Maintain appropriate portion sizes.

• Limit highly processed foods and sugary drinks.


💪 WORKOUT RECOVERY

• Have a balanced meal after exercise.

• Drink enough water before, during and after
  your workout.

• Give your muscles enough time to recover.

• Include rest or active-recovery days.

• Maintain a consistent sleep schedule.


⚡ FITNESS TIP

Consistency is important. Combine regular exercise,
balanced nutrition, hydration and adequate recovery
to support your fitness goals.


⚠️ NOTE

These are general fitness and nutrition suggestions.
Individual nutritional needs can vary.
"""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None,
            "nutrition": nutrition_result,
            "feedback_result": None,
        },
    )


# =========================================================
# FEEDBACK & UPDATE PLAN
# =========================================================

@router.post("/feedback", response_class=HTMLResponse)
async def feedback(
    request: Request,

    feedback_text: str = Form(...),

    goal: str = Form("general wellness"),

    fitness_level: str = Form("beginner"),

    days_per_week: int = Form(3),
):

    # -----------------------------------------------------
    # Use the feedback to modify the AI prompt
    # -----------------------------------------------------

    feedback_prompt = f"""
Create an updated personalized workout plan.

Fitness goal:
{goal}

Fitness level:
{fitness_level}

Training days per week:
{days_per_week}

User feedback:
{feedback_text}

The user wants the workout plan to be adjusted
according to their feedback.

Create a practical 7-day plan.

Include:
- Warm-up
- Exercises
- Sets
- Repetitions
- Rest periods
- Recovery days

Keep the plan suitable for the user's fitness level.
"""

    # -----------------------------------------------------
    # For now we create a clear updated plan.
    # This can later be connected directly to Gemini.
    # -----------------------------------------------------

    feedback_result = f"""
🔄 FITBUDDY AI - UPDATED WORKOUT PLAN

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USER FEEDBACK

"{feedback_text}"


FITNESS GOAL
{goal}


FITNESS LEVEL
{fitness_level}


TRAINING DAYS
{days_per_week} days per week


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UPDATED PLAN

DAY 1 - FULL BODY

• Warm-up: 5-10 minutes
• Squats: 3 × 10
• Push-ups: 3 × 10
• Dumbbell rows: 3 × 10
• Plank: 3 × 30 seconds


DAY 2 - CARDIO

• Walking or jogging: 20-30 minutes
• Light stretching: 5-10 minutes


DAY 3 - LOWER BODY

• Squats: 3 × 12
• Lunges: 3 × 10 each leg
• Glute bridges: 3 × 12
• Calf raises: 3 × 15


DAY 4 - RECOVERY

• Light walking
• Stretching
• Mobility exercises


DAY 5 - UPPER BODY

• Push-ups: 3 × 10
• Rows: 3 × 10
• Shoulder press: 3 × 10
• Biceps curls: 3 × 12


DAY 6 - CARDIO + CORE

• Cardio: 20 minutes
• Plank: 3 × 30 seconds
• Crunches: 3 × 15


DAY 7 - REST

• Rest
• Light stretching
• Recovery


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your feedback has been received and the workout
plan has been adjusted accordingly.
"""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None,
            "nutrition": None,
            "feedback_result": feedback_result,
        },
    )


# =========================================================
# COACH DASHBOARD
# =========================================================

@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):

    return HTMLResponse(
        """
        <!DOCTYPE html>

        <html>

        <head>

            <title>FitBuddy AI - Coach Dashboard</title>

            <style>

                body {
                    font-family: Arial, sans-serif;
                    background: #f4f7fb;
                    padding: 40px;
                }

                .box {
                    max-width: 800px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow:
                        0 10px 30px
                        rgba(0,0,0,0.08);
                }

                h1 {
                    color: #0d6efd;
                }

                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 15px;
                    background: #0d6efd;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                }

            </style>

        </head>

        <body>

            <div class="box">

                <h1>📊 FitBuddy AI Coach Dashboard</h1>

                <p>
                    User database and generated plan history
                    will appear here after database integration.
                </p>

                <a href="/">
                    ← Back to FitBuddy AI
                </a>

            </div>

        </body>

        </html>
        """
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
async def health_check():

    return {
        "status": "ok",
        "app": "FitBuddy AI"
    }