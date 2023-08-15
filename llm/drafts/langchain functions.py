import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0613")

function_descriptions = ...

user_request = """
Please do three things add 40 units to 2023 headcount
"""

first_response = llm.predict_messages([HumanMessage(content=user_request)],
                                      functions=function_descriptions)

print(first_response, '\n')
print(first_response.additional_kwargs)

function_name = first_response.additional_kwargs["function_call"]["name"]
print(function_name)
