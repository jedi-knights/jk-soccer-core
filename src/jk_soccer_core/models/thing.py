from pydantic import BaseModel


class Thing(BaseModel):
    name: str = None
    description: str = None
