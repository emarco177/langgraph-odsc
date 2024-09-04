from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                        You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet.
                        Always provide detailed recommendations, including requests for length, virality, style, etc.,
                        "Always return your answer in markdown format

                        ```markdown
                        **Original Tweet:** Just finished my first day back at work after vacation. Feeling kinda blah
                        
                        Answer:
                        **Grade:** 5/10

                        **Critique:** This tweet is a bit too generic. It lacks a hook to grab attention and doesn't really give us any insight
                        into your vacation or how you're feeling.

                        **Recommendations:**
                        - **Length:** Keep it under 280 characters for maximum impact.
                        - **Virality:** Try adding a question or call to action to encourage engagement. For example, "What's the best thing
                        you did on your last vacation?"
                        - **Style:** Use more descriptive language to paint a picture for your followers. Instead of 'kinda blah,' try
                        something like 'overwhelmed by the return to reality' or 'missing the sunshine and cocktails.'
            
                        **Original Tweet:**: {tweet}
            """,
        ),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with revising twitter posts according"
            " to feedback from the previous message ."
            "Revise the current tweet according te critique to the best twitter post possible."
            "{critique}"
            "You ONLY should respond with a revised version of the tweet."
            "**current tweet:** {tweet}"
            "There is not need for markdown format, only write the tweet and do not write the critique"
            "**New Tweet:** ",
        ),
    ]
)


llm = ChatOllama(model="gemma2")
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
