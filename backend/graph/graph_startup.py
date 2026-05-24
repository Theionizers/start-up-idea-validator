from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
from graph.output_parser import startupanalysis,comp_find_analysis,score,FundingCompanies

from langchain_tavily import TavilySearch
search_tool = TavilySearch(max_results=5)
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

structured_llm=llm.with_structured_output(
    startupanalysis
)
fund_llm=llm.with_structured_output(
    FundingCompanies
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
    growth:str
    funding_comp:list[str]

def idea_analyzer(state: GraphState):

    print("INSIDE IDEA ANALYZER")

    idea = state["idea"]

    prompt = f"""
    Analyze this startup idea:
    {idea}
    """

    response = structured_llm.invoke(prompt)

    print(response)

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
        "competitors": response.competitors
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


def scoreing(state:GraphState):
    if(state["final_score"]>=50):
      return "fund_node"
    else: return "improvement_node"

def fund_node(state: GraphState):

    search_results = search_tool.invoke(
        f"Top investors for {state['idea']} startup"
    )

    prompt = f"""
    Extract funding companies and investors from this data:

    {search_results}

    Return only company names.
    """

    response = fund_llm.invoke(prompt)

    return {
        "funding_comp": response.companies
    }

def improvement_node(state: GraphState):

    print("INSIDE IMPROVEMENT NODE")

    prompt = f"""
    You are a startup mentor.

    This startup idea received a low score.

    Startup Idea:
    {state["idea"]}

    Target Users:
    {state["target_users"]}

    Budget:
    {state["budget"]}

    Analysis:
    {state["analysis"]}

    Competitors:
    {state["competitors"]}

    

    

    Give detailed improvement suggestions for:

    1. product idea
    2. target audience
    3. monetization
    4. market positioning
    5. budget optimization
    6. scalability
    7. differentiation from competitors

    Also give:
    - an improved startup version
    - MVP suggestion
    - go-to-market strategy
    """

    response = llm.invoke(prompt)

    print(response.content)

    return {
        "recommendation": response.content
    }

graph_builder = StateGraph(GraphState)

graph_builder.add_node(
    "idea_analyzer",
    idea_analyzer
)

graph_builder.add_node(
    "fund_node",
    fund_node
)
graph_builder.add_node(
    "improvement_node",
    improvement_node
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

graph_builder.add_conditional_edges(
    "scoring_agent",
    scoreing,
    {
        "fund_node": "fund_node",
        "improvement_node": "improvement_node"
    }
)
graph_builder.add_edge(
    "fund_node",
    END
)
graph_builder.add_edge(
    "improvement_node",
    END
)

startup_graph = graph_builder.compile()
print(startup_graph.get_graph().draw_mermaid())