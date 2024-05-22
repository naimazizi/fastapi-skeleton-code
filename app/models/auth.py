from pydantic import BaseModel
from typing import Optional, Set


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str


class TagRoles:
    tag: str
    roles: Set[str]
