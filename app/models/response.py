from pydantic import BaseModel
from datetime import datetime


class DatetimeValue(BaseModel):
    datetime: datetime
    value: int = 0


class CategoricalValue(BaseModel):
    category: str
    value: int = 0
