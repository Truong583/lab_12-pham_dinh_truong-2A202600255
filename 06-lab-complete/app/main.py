"""
Production AI Agent (Ultra Edition) — Lab 12 Final Masterpiece.
Features: JWT, Redis Stateless Design, Conversation History.
"""
import time
import signal
import logging
import json
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from app.config import settings
from app.auth import get_current_user, create_access_token, verify_api_key
from app.rate_limiter import limiter
from app.cost_guard import guardian
from app.history import history_manager
from utils.mock_llm import ask as llm_ask

# ─────────────────────────────────────────────────────────
# Logging — JSON structured
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False

# ─────────────────────────────────────────────────────────
# Lifespan
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info(json.dumps({
        "event": "startup",
        "app": settings.app_name,
        "port": settings.port,
        "redis_connected": bool(settings.redis_url),
        "environment": settings.environment,
    }))
    time.sleep(0.1)
    _is_ready = True
    yield
    _is_ready = False
    logger.info(json.dumps({"event": "shutdown"}))

# ─────────────────────────────────────────────────────────
# App & Middleware
# ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

# ─────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)

class AskResponse(BaseModel):
    question: str
    answer: str
    history_count: int
    timestamp: str

# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "AI Agent Ultra API - Day 12 Final", "status": "online"}

@app.post("/login", tags=["Auth"])
async def login(api_key: str = Depends(verify_api_key)):
    """Đổi API Key lấy JWT Token (hết hạn sau 60 phút)"""
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    access_token = create_access_token(
        data={"sub": "admin"},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/ask", response_model=AskResponse, tags=["Agent"])
async def ask_agent(
    body: AskRequest,
    user_id: str = Depends(get_current_user),
):
    # 1. Rate limit (Dùng Redis)
    limiter.check(user_id)

    # 2. Lấy lịch sử (Dùng Redis)
    history = history_manager.get_history(user_id)
    
    # 3. Giả lập đưa lịch sử vào prompt (Stateless context)
    context_prompt = f"Lịch sử: {len(history)} tin nhắn. Câu hỏi: {body.question}"
    
    # 4. Budget check & AI Call
    guardian.check_and_record_cost(len(body.question), 0)
    answer = llm_ask(context_prompt)
    guardian.check_and_record_cost(0, len(answer))

    # 5. Lưu lịch sử mới vào Redis
    history_manager.add_message(user_id, "user", body.question)
    history_manager.add_message(user_id, "assistant", answer)

    return AskResponse(
        question=body.question,
        answer=answer,
        history_count=len(history),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

@app.get("/health", tags=["Ops"])
def health():
    return {"status": "ok", "uptime": round(time.time() - START_TIME, 1)}

@app.get("/ready", tags=["Ops"])
def ready():
    if not _is_ready: raise HTTPException(503, "Not ready")
    return {"ready": True}

# ─────────────────────────────────────────────────────────
# Signal Handler
# ─────────────────────────────────────────────────────────
def _handle_signal(signum, _frame):
    logger.info(json.dumps({"event": "signal", "signum": signum}))

signal.signal(signal.SIGTERM, _handle_signal)

if __name__ == "__main__":
    logger.info(f"🚀 Starting {settings.app_name} on {settings.host}:{settings.port}")
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
