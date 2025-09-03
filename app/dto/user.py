from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
