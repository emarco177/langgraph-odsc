import operator
import time
from random import random, randint
from typing import Annotated, Any, Dict

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    # The operator.add reducer fn makes this append-only
    aggregate: Annotated[list, operator.add]


class ReturnNodeValue:
    def __init__(self, value: str):
        self._value = value

    def __call__(self, state: State) -> Any:
        time.sleep(randint(1, 5))
        print("****")
        print(f"Adding `{self._value}` to {state['aggregate']}")
        return {"aggregate": [self._value]}


def hello(state: State) -> Dict[str, Any]:
    print("hello")
    return {"aggregate": ["hello"]}


def welcome(state: State) -> Dict[str, Any]:
    print("welcome")
    return {"aggregate": ["welcome"]}


def to(state: State) -> Dict[str, Any]:
    print("to")
    return {"aggregate": ["to"]}


def ODSC(state: State) -> Dict[str, Any]:
    print("ODSC")
    return {"aggregate": ["ODSC"]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("Hello"))
builder.add_node("b", ReturnNodeValue("welcome"))
builder.add_node("c", ReturnNodeValue("to"))
builder.add_node("d", ReturnNodeValue("ODSC!"))
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "d")
builder.add_edge("c", "d")
builder.add_edge("d", END)
graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    res = graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
    print(res["aggregate"])
