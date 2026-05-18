from fastapi import FastAPI
from models.schemas import IdeaRequest
from graph.graph_startup import startup_graph
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}

@app.post("/validate")
async def validate_idea(data: IdeaRequest):

    result = startup_graph.invoke({
        "idea": data.idea,
        "target_users":data.target_users,
        "budget":data.budget
    })

    return result