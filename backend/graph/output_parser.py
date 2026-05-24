from pydantic import BaseModel
from typing import List

class startupanalysis(BaseModel):
    summary:str
    target_users:str
    strengths:list[str]
    weakness:list[str]
    

class comp_find_analysis(BaseModel):
    competitors:List[str]

class score(BaseModel):
    final_score:int
    recommendation:str
class FundingCompanies(BaseModel):
    companies: List[str]