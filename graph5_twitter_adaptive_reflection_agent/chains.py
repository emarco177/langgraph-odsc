from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

publish_tweet_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a social media strategist analyzing a potential tweet.  Determine if a tweet is ready to be published or needs
            revision based on the following criteria:
            
            * **Engageability:** Does the tweet spark conversation? Does it ask a question, offer a thought-provoking statement, or
            use humor/emotion to connect with users?
            * **Virality:** Does the tweet have the potential to spread widely? Is it timely, relevant to current trends, or easily
            shareable?
            * **Brevity:**  Is the tweet concise and to the point? Does it convey its message effectively within the 280 character
            limit?
            
                        
             Provide the following analysis:
            
            1. **Verdict:** "Publish" or "Revision Needed"
            2. **Reasoning:** A brief explanation outlining your decision based on the three criteria.
            
            **Tweet** {tweet}
            """,
        )
    ]
)
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


class Verdict(BaseModel):
    publish: bool = Field(description="True if can Publish or False if Revision Needed")
    reasoning: str = Field(
        description="A brief explanation outlining your decision based on the three criteria"
    )

publish_tweet_chain = publish_tweet_prompt | llm | StrOutputParser()




