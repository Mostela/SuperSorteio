from typing import List

from pydantic import BaseModel


class ProfileGame(BaseModel):
    keyGame: str
    guidUser: str
    numberList: List[int]
