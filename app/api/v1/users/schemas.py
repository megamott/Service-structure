from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    ...


class User(UserBase):
    ...
