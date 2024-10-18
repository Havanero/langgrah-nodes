from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class InputState(TypedDict):
    user_question: str

class OutputState(TypedDict):
    reply: str
class OverallState(TypedDict):
    look_up: str
    user_question: str
    reply: str
class PrivateState(TypedDict):
    process: str

def greeter(state: InputState) -> OverallState:
    return {"look_up": state["user_question"]}

def processor(state: OverallState) -> PrivateState:
    def do_process(state):
        print("processing user input", state["look_up"])
        return "Tickets will be made available in the next 24hrs"
    return {"process": do_process(state)}

def assistant(state: PrivateState) -> OutputState:
    return {"reply": state["process"]}

workflow = StateGraph(OverallState, input=InputState, output=OutputState)

workflow.add_node("greeter", greeter)
workflow.add_node("processor", processor)
workflow.add_node("assistant", assistant)
workflow.add_edge(START, "greeter")
workflow.add_edge("greeter", "processor")
workflow.add_edge("processor", "assistant")
workflow.add_edge("assistant", END)

app = workflow.compile()
