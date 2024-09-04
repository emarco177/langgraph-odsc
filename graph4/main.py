import operator
from typing import TypedDict, Annotated, Dict, Any

from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import END, StateGraph

from chains import generate_chain, reflect_chain


class State(TypedDict):
    messages: Annotated[list, operator.add]
    tweet: str
    original_tweet: str
    critique: str
    revised_tweet: str
    iterations: int


REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: State) -> Dict[str, Any]:
    res = generate_chain.invoke(
        {"tweet": state["tweet"], "critique": state["critique"]}
    )
    return {"revised_tweet": res.content, "iterations": int(state["iterations"]) + 1}


def reflection_node(state: State) -> Dict[str, Any]:
    res = reflect_chain.invoke({"tweet": state["tweet"]})
    return {
        "critique": res.content,
    }


builder = StateGraph(State)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(REFLECT)

builder.add_node(GENERATE, generation_node)


def should_continue(state: Dict[str, Any]):
    if int(state["iterations"]) >= 2:
        return END
    return GENERATE


builder.add_conditional_edges(REFLECT, should_continue)
builder.add_edge(GENERATE, REFLECT)

graph = builder.compile()
# graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print("Hello LangGraph")
    tweet = """
            
            @LangChainAI
            — newly Tool Calling feature is underrated.
            After a long wait, it's  here- making the implementation of agents across different models
            with function calling - super easy.
    """

    for state in graph.stream(
        {"tweet": tweet, "revised_tweet": tweet, "iterations": 0},
        {"configurable": {"thread_id": "odsc_userid_12844"}},
        stream_mode="values",
    ):
        print(f"{state=}")
