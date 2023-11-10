from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreateValidator(UserBase):
    ...


class UserIdValidator(BaseModel):
    id: int


class UserSerializator(UserBase):
    id: int
