from typing import Dict, Optional, Set


class Auth():
    _instance = None
    _dict: Dict[str, Set[str]] = dict()

    @classmethod
    def get_roles(cls, tag: str) -> Optional[Set[str]]:
        return cls._dict.get(tag)

    @classmethod
    def is_eligible(cls, tag: str, role: str) -> bool:
        _roles = cls.get_roles(tag)
        if _roles is None:
            return False
        else:
            return role in _roles

    @classmethod
    async def set_cache(
            cls, dictionary: Dict[str, Set[str]]
            ) -> None:
        if cls._instance is None:
            raise RuntimeError('Class instance is not found')
        else:
            cls._dict = await dictionary

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Auth, cls).__new__(cls)
        return cls._instance


auth = Auth()
