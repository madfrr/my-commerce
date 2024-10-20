from pydantic import BaseModel
from typing import List


class CreateUserResponse(BaseModel):
    id: str


class CreateUser(BaseModel):
    name: str
    email: str


class UpdateUser(BaseModel):
    id: str
    name: str | None
    email: str | None


class UserDTO(BaseModel):
    id: str | None = None
    name: str | None = None
    email: str | None = None


class ListUserDTO(BaseModel):
    data: List[UserDTO]


class FilterParams(BaseModel):
    id: str | None = None
    email: str | None = None
