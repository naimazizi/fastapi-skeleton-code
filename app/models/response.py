from pydantic import BaseModel
from datetime import datetime
from typing import Any


class DatetimeValue(BaseModel):
    datetime: datetime
    value: int = 0


class CategoricalValue(BaseModel):
    category: str
    value: int = 0


class ResponseModel:
    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self.data = data

    @property
    def get_data(self):
        return self.data

    @property
    def get_status_code(self):
        return self.status_code
