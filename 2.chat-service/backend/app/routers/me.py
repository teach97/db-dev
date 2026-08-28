from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db import get_anon_client
from app.deps import CurrentUser, get_current_user
from app.schemas import (
    ConversationOut,
    MessageCreate,
    MessageOut,
    MyConversationCreate,
    ProfileOut,
    ProfileUpdate,
)

router = APIRouter(prefix="/me", tags=["me"])


@router.get("")
def read_me(current_user: CurrentUser = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}


@router.get("/conversations", response_model=list[ConversationOut])
def my_conversations(current_user: CurrentUser = Depends(get_current_user)):
    client = get_anon_client()
    client.postgrest.auth(current_user.token)
    result = (
        client.table("conversations")
        .select("*")
        .eq("user_id", current_user.id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data

# 내 프로필 조회
@router.get("/profile", response_model=ProfileOut)
def read_my_profile(current_user: CurrentUser = Depends(get_current_user)):
    client = get_anon_client()
    client.postgrest.auth(current_user.token)
    result = client.table("profiles").select("*").execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")
    return result.data[0]


# 문제 2. 내 닉네임 수정
@router.patch("/profile", response_model=ProfileOut)
def update_my_profile(
    payload: ProfileUpdate,
    current_user: CurrentUser = Depends(get_current_user),
):
    client = get_anon_client()
    client.postgrest.auth(current_user.token)
    try:
        result = (
            client.table("profiles")
            .update({"username": payload.username})
            .eq("id", current_user.id)
            .select("*")
            .execute()
        )
    except Exception as e:
        # 개발 중에는 터미널에서도 실제 Supabase 오류를 확인할 수 있게 한다.
        print(f"[PATCH /me/profile] {type(e).__name__}: {e}")
        raise HTTPException(status_code=400, detail=f"프로필 수정 실패: {e}")
    if not result.data:
        raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다")
    return result.data[0]


# 문제 3. 토큰 기반 내 대화 생성
@router.post("/conversations", response_model=ConversationOut, status_code=201)
def create_my_conversation(
    payload: MyConversationCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    client = get_anon_client()
    client.postgrest.auth(current_user.token)
    result = (
        client.table("conversations")
        .insert({"user_id": current_user.id, "title": payload.title})
        .execute()
    )
    return result.data[0]


# 문제 4. 남의 대화에 메시지 넣기 방지
@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageOut,
    status_code=201,
)
def create_my_message(
    conversation_id: UUID,
    payload: MessageCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    client = get_anon_client()
    client.postgrest.auth(current_user.token)
    try:
        result = (
            client.table("messages")
            .insert(
                {
                    "conversation_id": str(conversation_id),
                    "role": payload.role,
                    "content": payload.content,
                }
            )
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=403, detail="이 대화에 접근할 수 없습니다")
    return result.data[0]
