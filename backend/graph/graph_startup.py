from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
from graph.output_parser import startupanalysis,comp_find_analysis,score
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

structured_llm=llm.with_structured_output(
    startupanalysis
)
comp_llm=llm.with_structured_output(
    comp_find_analysis
)
score_llm=llm.with_structured_output(
    score   
)
class GraphState(TypedDict):
    idea: str
    target_users: str
    budget: int
    analysis: dict
    competitors:list[str]
    final_score:int 
    recommendation:str

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
def comp_find(state:GraphState):
    prompt = f"""
    Find competitors for this startup idea:

    {state["idea"]}

    Return competitor names only.
    """

    response = comp_llm.invoke(prompt)

    

    return {
        "competitors": response
    }

def scoring_agent(state: GraphState):

    prompt = f"""
    Evaluate this startup idea.

    Idea:
    {state["idea"]}

    Analysis:
    {state["analysis"]}

    Competitors:
    {state["competitors"]}

    Budget:
    {state["budget"]}

    Give:
    - startup score out of 100
    - risk level
    - feasibility
    - recommendation
    """

    response = score_llm.invoke(prompt)

    return response.model_dump()


# ---------------------------
# GRAPH
# ---------------------------

graph_builder = StateGraph(GraphState)

graph_builder.add_node(
    "idea_analyzer",
    idea_analyzer
)
graph_builder.add_node(
    "competitors",
    comp_find
)
graph_builder.add_node(
    "scoring_agent",
    scoring_agent
)

graph_builder.add_edge(
    START,
    "idea_analyzer"
)
graph_builder.add_edge(
    "idea_analyzer",
    "competitors",
)
graph_builder.add_edge(
    "competitors",
    "scoring_agent",
)
graph_builder.add_edge(
    "scoring_agent",
    END
)

startup_graph = graph_builder.compile()