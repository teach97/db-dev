"""FastAPI 앱 진입점.

실행:  uv run uvicorn app.main:app --reload
확인:  http://127.0.0.1:8000/health  ·  http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

app = FastAPI(title="chat-service", version="0.1.0")


# 현재 실습 범위에서는 대화 라우터를 등록한다.
# users 라우터는 아직 실습 TODO 상태이므로 지금 등록하면 import 오류가 날 수 있다.
from app.routers import auth, conversations, me
app.include_router(conversations.router)
app.include_router(auth.router)
app.include_router(me.router)

@app.get("/health")
def health():
    return {"status": "ok"}
