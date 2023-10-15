from typing import List, Union, Type

from langchain.schema import HumanMessage, AIMessage, FunctionMessage


Message = Type[Union[HumanMessage, AIMessage, FunctionMessage]]