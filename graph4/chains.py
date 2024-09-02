from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with revising twitter posts according to feedback."
            "Revise the current tweet to the best twitter post possible."
            "You should respond with a revised version of the tweet."
            "Revised tweet: ",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


llm = ChatOllama(model="gemma2")
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
