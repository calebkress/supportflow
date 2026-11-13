
from fastapi import FastAPI

from app.config import settings
from app.api.tickets import router as tickets_router


app = FastAPI(
    title=settings.app_name,
    description="AI-assisted infrastructure support automation",
    version="0.1.0",
)

app.include_router(tickets_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
