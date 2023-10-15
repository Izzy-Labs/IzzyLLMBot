import json

from typing import List

from langchain.schema import HumanMessage, AIMessage, FunctionMessage

from .types import Message     # see telegram/llm/_types.py


def chat_to_json(messages: List[Message]) -> str:
    messages_to_json = []
    if messages:
        for message in messages:
            message_type = message.__class__.__name__
            content = message.content
            messages_to_json.append({
                'message_type': message_type,
                'content': content
            })

    return json.dumps(messages_to_json)


def json_to_chat(json_str: str) -> List[Message]:
    messages = json.loads(json_str)
    messages_to_return = []

    for message in messages:
        message_type = message['message_type']
        content = message['content']

        if message_type == 'HumanMessage':
            messages_to_return.append(HumanMessage(content=content))
        elif message_type == 'AIMessage':
            messages_to_return.append(AIMessage(content=content))
        elif message_type == 'FunctionMessage':
            messages_to_return.append(FunctionMessage(content=content))
        else:
            raise TypeError(f'Unknown message type: {message_type}')

    return messages_to_return
