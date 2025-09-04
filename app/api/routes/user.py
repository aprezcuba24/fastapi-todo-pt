from fastapi import APIRouter
from app.api.dependencies import SessionDep
from app.dto import UserCreate, UserResponse, UserLogin
from app.services import find_by_username, create_user, get_token
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def register(user_in: UserCreate, session: SessionDep):
    if await find_by_username(session, user_in.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = await create_user(session, user_in)
    return user


@router.post("/login")
async def login(user_in: UserLogin, session: SessionDep):
    token = await get_token(session, user_in)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": token}
