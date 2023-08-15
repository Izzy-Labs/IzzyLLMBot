import json

from langchain.chat_models import ChatOpenAI


LLM = ChatOpenAI(model="gpt-3.5-turbo-0613")

with open('llm/function_descriptions.json', 'r') as file:
    function_descriptions = json.load(file)
