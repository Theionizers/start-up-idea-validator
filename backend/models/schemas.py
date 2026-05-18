from pydantic import BaseModel

class IdeaRequest(BaseModel):
    idea: str
    target_users: str
    budget: int

