from dotenv import load_dotenv
from textwrap import dedent
from phi.agent import Agent
from phi.model.together import Together
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class Tweet(BaseModel):
    text: str = Field(..., description="This is the tweet")

class Threadx(BaseModel):
    tweets: List[str] = Field(..., description="This is a list of tweets.")

#Get the Essay
def get_essay(mail_body, api_key):
    text_parser_assistant = Agent(
            name="TextParserAssistant",
            model=Together(id="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",api_key=api_key),
            description=dedent(
                """
                You are a content parser.
                """
            ),
            instructions=[
                    "IMPORTANT: Parse the content and extract the text out from the html code.",
                    "IMPORTANT: Output should be in simple text format and MUST NOT CONTAIN html tag.",
                    "IMPORTANT: Once the text is extracted only contain information about a single news and ignore the other news"
            ],
            markdown=True
        )
    parsedText= text_parser_assistant.run("Parse the content, extract the text from this html code: {0}".format(mail_body),markdown=True,stream=False).content
    
    essay_assistant= Agent(
            name="EssayAssistant",
            model=Together(id="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",api_key=api_key),
            description=dedent(
                """
                You are a world-class essay writer, able to transform complex ideas into clear, compelling narratives with precision and depth. 
                Your writing demonstrates a mastery of language, a commitment to thorough research, and an ability to engage readers, 
                leaving a lasting impact on those who seek insight and clarity on diverse topics.
                """
            ),
            instructions=[
                    "IMPORTANT: Come up with a comprehensive essay of what is being talked about in the content, make sure their is only single context in the essay. focus only on one main news and ignore the other news",
                    "IMPORTANT: Only talk about a single news topic and do not mix topics.",
                    "IMPORTANT: Do not mention anything about any article, we want to ensure that this essay is written by me only."
            ],
            markdown=True
        )
    return essay_assistant.run("Create a 200 word essay for {0}".format(parsedText),stream=False,markDown=True).content

#Create a twitter thread
def get_twitter_thread(essay,source,api_key):
    twitter_thread_assistant = Agent(
            name="TwitterThreadAssistant",
            model=Together(id="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",api_key=api_key),
            description=dedent(
                """
                You are a viral twitter thread cretor who will be writing catchy twitter thread on my behalf.
                """
            ),
            instructions=[
                    "IMPORTANT: Convert the given essay into a list of 6-10 tweets thread.In the last tweet give credits to {0} for the information.".format(source),
                    "IMPORTANT: Preceed the tweet with a tweet number and each sentence length should be less than 260 characters and do not include the word essay in it.",
            ],
            response_model=Threadx
        )
    thread_json = twitter_thread_assistant.run("Create a nice twitter thread of 6-8 tweets for this essay:{0}".format(essay),stream=False).content
    return thread_json

# Summarise tweet
def get_tweet_summary(tweet, charlen, api_key):
    summarise_agent = Agent(
            name="SummariseAssistant",
            model=Together(id="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",api_key=api_key),
            description=dedent(
                """
                You are sentence summariser.
                """
            ),
            instructions=[
                    "IMPORTANT: Summarise the sentence in less than {0} characters.".format(charlen),
            ],
            markdown=True
        )
    return summarise_agent.run("Create a summary for this sentence : {0} in less thant {1} characters.".format(tweet,charlen),stream=False,markDown=True).content
    