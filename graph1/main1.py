# Simply Graph
# make to audienc that we are working onlanggraph constructs, not building graph
# show functions implementation

# make colab
import operator
import time
from typing import Annotated, Any, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]


def hello(state: State) -> Dict[str, Any]:
    print("#### hello enter,")
    time.sleep(1)
    return {"aggregate": ["hello"]}


def welcome(state: State) -> Dict[str, Any]:
    print("#### welcome enter,")
    time.sleep(1)
    return {"aggregate": ["welcome"]}


def to(state: State) -> Dict[str, Any]:
    print("#### to enter,")
    time.sleep(1)
    return {"aggregate": ["to"]}


def odsc(state: State) -> Dict[str, Any]:
    print("#### odsc enter,")
    time.sleep(1)
    return {"aggregate": ["ODSC"]}


builder = StateGraph(State)
builder.add_node("a", hello)
builder.add_node("b", welcome)
builder.add_node("c", to)
builder.add_node("d", odsc)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", "c")
builder.add_edge("c", "d")
builder.add_edge("d", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
    # res = graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
    # print(f"{res=}")

    for state in graph.stream({"aggregate": []}, {"configurable": {"thread_id": "foo"}}, stream_mode="values"):
        print(f"{state=}")
