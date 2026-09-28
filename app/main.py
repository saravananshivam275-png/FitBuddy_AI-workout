from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(
    title="FitBuddy AI",
    description="AI-powered personalized fitness planner",
    version="1.0.0",
)


# Static files
static_directory = BASE_DIR / "static"

if static_directory.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(static_directory)),
        name="static",
    )


# Application routes
app.include_router(router)