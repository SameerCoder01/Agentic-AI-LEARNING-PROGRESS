
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# ==================================
# 1. DEFINE AGENT STATE
# ==================================

class AgentState(TypedDict):
    task: str
    document: str
    extracted_text: str
    analysis: str
    report: str


# ==================================
# 2. DEFINE NODES
# ==================================

def load_document(state: AgentState):

    print("Loading document...")

    return {
        "document": "research_paper.pdf"
    }


def extract_text(state: AgentState):

    print("Extracting text...")

    return {
        "extracted_text": "AI improves healthcare through machine learning."
    }


def analyze_document(state: AgentState):

    print("Analyzing document...")

    return {
        "analysis": "The paper discusses AI applications in healthcare."
    }


def generate_report(state: AgentState):

    print("Generating report...")

    return {
        "report": "Final Report: AI has important applications in healthcare."
    }


# ==================================
# 3. CREATE GRAPH
# ==================================

workflow = StateGraph(AgentState)


# ==================================
# 4. ADD NODES
# ==================================

workflow.add_node("load", load_document)
workflow.add_node("extract", extract_text)
workflow.add_node("analyze", analyze_document)
workflow.add_node("report", generate_report)


# ==================================
# 5. ADD EDGES
# ==================================

workflow.add_edge(START, "load")
workflow.add_edge("load", "extract")
workflow.add_edge("extract", "analyze")
workflow.add_edge("analyze", "report")
workflow.add_edge("report", END)


# ==================================
# 6. COMPILE GRAPH
# ==================================

app = workflow.compile()


# ==================================
# 7. INITIAL STATE
# ==================================

initial_state: AgentState = {
    "task": "Analyze research paper",
    "document": "",
    "extracted_text": "",
    "analysis": "",
    "report": ""
}


# ==================================
# 8. EXECUTE WORKFLOW
# ==================================

result = app.invoke(initial_state)


print("\n--- FINAL RESULT ---")
print(result)
