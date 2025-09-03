from fastapi import APIRouter
from app.api.dependencies import SessionDep
from app.dto import UserCreate, UserResponse
from app.services.user import find_by_username, create_user
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def register(user_in: UserCreate, session: SessionDep):
    if find_by_username(session, user_in.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = create_user(session, user_in)
    return user
