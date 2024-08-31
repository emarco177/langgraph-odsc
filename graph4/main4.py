# Conditional Branch
import datetime
import operator
import time
from typing import Annotated, Any, Dict, Sequence, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END





def node_a(state: State) -> Dict[str, Any]:
    print("#### node_a enter,")
    time.sleep(1)
    return {"aggregate": ["node_a"]}


def node_b(state: State) -> Dict[str, Any]:
    print("#### node_b enter,")
    time.sleep(1)
    return {"aggregate": ["node_b"]}


def node_c(state: State) -> Dict[str, Any]:
    print("#### node_c enter,")
    time.sleep(1)
    return {"aggregate": ["node_c"]}


def node_d(state: State) -> Dict[str, Any]:
    print("#### node_d enter,")
    time.sleep(1)
    return {"aggregate": ["node_d"]}


def node_e(state: State) -> Dict[str, Any]:
    print("#### node_e enter,")
    time.sleep(1)
    return {"aggregate": ["node_e"]}


def route(state: State) -> List[str]:
    if datetime.datetime.utcnow().second % 2 == 0:
        return ["node_b"]
    return ["node_c", "node_d"]


builder = StateGraph(State)
intermediates = ["node_b", "node_c", "node_d"]
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)
builder.add_node("node_d", node_d)
builder.add_node("node_e", node_e)

builder.add_edge(START, "node_a")
builder.add_edge("node_e", END)
builder.add_conditional_edges("node_a", route, intermediates)
for node in intermediates:
    builder.add_edge(node, "node_e")
graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
    res = graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
    print(f"{res=}")
