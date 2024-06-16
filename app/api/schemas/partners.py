from pydantic import BaseModel


class Partners(BaseModel):
    id: int
    path_logo: str
    place: int
