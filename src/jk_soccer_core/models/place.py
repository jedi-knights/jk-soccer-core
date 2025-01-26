from pydantic import BaseModel


class Place(BaseModel):
    name: str = None
