from typing import Dict, Optional, Set, List
import jwt
from loguru import logger

from app import setting


SECRET_KEY = setting.JWT_SECRET_KEY
ALGORITHM = setting.JWT_ALGORITHM


class Auth:
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
    def set_cache(cls, dictionary: Dict[str, Set[str]]) -> None:
        if cls._instance is None:
            raise RuntimeError("Class instance is not found")
        else:
            cls._dict = dictionary

    # TODO: add this method to is_eligible.
    def decode_jwt(
        self,
        jwt_string: str,
        secret_key: str = SECRET_KEY,
        algorithm: List[str] = [ALGORITHM],
    ) -> Optional[Dict]:
        payload = None
        try:
            payload = jwt.decode(jwt_string, secret_key, algorithms=algorithm)
        except jwt.PyJWTError:
            logger.opt(exception=True).error(
                "Error in decoding jwt token using " "secret key: {} and algorithms {}",
                secret_key,
                ",".join(algorithm),
            )
        return payload

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Auth, cls).__new__(cls)
        return cls._instance


auth = Auth()
