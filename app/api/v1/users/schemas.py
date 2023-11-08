from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreateValidator(UserBase):
    ...


class UserValidator(UserBase):
    id: int


class UserIdValidator(BaseModel):
    id: int
