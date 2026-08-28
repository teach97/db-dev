from fastapi import APIRouter, HTTPException

from app.db import get_anon_client
from app.schemas import LoginRequest, SignupRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse)
def signup(payload: SignupRequest):
    client = get_anon_client()
    try:
        result = client.auth.sign_up(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not result.user:
        raise HTTPException(status_code=400, detail="회원가입한 사용자를 확인할 수 없습니다")

    access_token = result.session.access_token if result.session else None
    return TokenResponse(
        access_token=access_token,
        user_id=result.user.id,
        email=result.user.email,
        message=None if result.session else "이메일 인증 후 로그인하세요",
    )

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    client = get_anon_client()
    try:
        result = client.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    if not result.user or not result.session:
        raise HTTPException(status_code=401, detail="로그인 세션을 만들 수 없습니다")

    return TokenResponse(
        access_token=result.session.access_token,
        user_id=result.user.id,
        email=result.user.email,
    )
