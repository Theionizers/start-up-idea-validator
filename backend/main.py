from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from models.schemas import IdeaRequest
from graph.graph_startup import startup_graph

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/validate")
def validate_idea(request: IdeaRequest):
    print("REQUEST RECEIVED")

    result = startup_graph.invoke({
        "idea": request.idea,
        "target_users": request.target_users,
        "budget": request.budget
    })  # type: ignore[arg-type]

    print("GRAPH FINISHED")

    return result

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return FileResponse(frontend_dir / "index.html")