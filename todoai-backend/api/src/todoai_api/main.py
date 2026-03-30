from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, calendar, tasks, users

app = FastAPI(title="todoai API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(calendar.router, prefix="/api/v1/calendar", tags=["calendar"])


@app.get("/health")
def health():
    return {"status": "ok"}
