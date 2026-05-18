from pydantic import BaseModel
from typing import List

class startupanalysis(BaseModel):
    summary:str
    target_users:str
    strengths:list[str]
    weakness:list[str]
    score:int