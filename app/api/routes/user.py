from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def register():
    return {"message": "User registered successfully"}
