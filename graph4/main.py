from typing import List, Sequence

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generate_chain, reflect_chain


REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]


builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(REFLECT)


def should_continue(state: List[BaseMessage]):
    if len(state) > 4:
        return END
    return REFLECT


builder.add_conditional_edges(REFLECT, should_continue)
builder.add_edge(GENERATE, REFLECT)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print("Hello LangGraph")
    inputs = HumanMessage(
        content="""Tweet:
                                    @LangChainAI
            — newly Tool Calling feature is seriously underrated.

            After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.
                                  """
    )
    response = graph.invoke(inputs)
    print(response)
    # for state in graph.stream(inputs, {"configurable": {"thread_id": "foo"}}, stream_mode="values"):
    #     print(f"{state=}")
