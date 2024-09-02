# Async
import operator
import time
from typing import Annotated, Any, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]


def node_a(state: State) -> Dict[str, Any]:
    print("#### node_a enter,")
    time.sleep(1)
    return {"aggregate": ["hello"]}


def node_b(state: State) -> Dict[str, Any]:
    print("#### node_b enter,")
    time.sleep(1)
    return {"aggregate": ["welcome"]}


def node_c(state: State) -> Dict[str, Any]:
    print("#### node_c enter,")
    time.sleep(3)
    return {"aggregate": ["to"]}


def node_d(state: State) -> Dict[str, Any]:
    print("#### d enter,")
    time.sleep(1)
    return {"aggregate": ["ODSC"]}


def b2(state: State) -> Dict[str, Any]:
    print("#### b2 enter,")
    time.sleep(5)
    return {"aggregate": ["!!!"]}


builder = StateGraph(State)
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("b2", b2)
builder.add_node("c", node_c)
builder.add_node("d", node_d)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b2")
builder.add_edge(["b2", "c"], "d")
builder.add_edge("d", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
    res = graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
    print(f"{res=}")
