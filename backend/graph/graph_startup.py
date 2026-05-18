from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
from graph.output_parser import startupanalysis
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

structured_llm=llm.with_structured_output(
    startupanalysis
)
class GraphState(TypedDict):
    idea: str
    target_users: str
    budget: int
    analysis: dict
def idea_analyzer(state: GraphState):

    idea = state["idea"]
    target_users=state["target_users"]
    budget=state["budget"]

    prompt = f"""
    Analyze this startup idea:

    {idea}
    and {target_users} and {budget}
    Give:
    - summary
    - target users
    - strengths
    """

    response = structured_llm.invoke(prompt)

    return {
        "analysis": response.model_dump()
    }


# ---------------------------
# GRAPH
# ---------------------------

graph_builder = StateGraph(GraphState)

graph_builder.add_node(
    "idea_analyzer",
    idea_analyzer
)

graph_builder.add_edge(
    START,
    "idea_analyzer"
)

graph_builder.add_edge(
    "idea_analyzer",
    END
)

startup_graph = graph_builder.compile()