from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="StayMate AI Hotel Assistant",
    description="Backend API for the StayMate Grand Hotel guest assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://dhayanand458.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "staymate-ai-backend",
    }