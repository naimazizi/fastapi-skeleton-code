from pydantic import BaseModel
from typing import Set


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None
    role: str


class TagRoles():
    tag: str
    roles: Set[str]
