from pydantic import BaseModel
from datetime import date


class Event(BaseModel):
    date: date
