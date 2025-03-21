import json
from openai import OpenAI
from tool import get_tool_schemas, get_tool_function
from typing import Any, Dict, List, Tuple

def get_tools() -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """OpenAI tool schema wrapper"""
    functions = get_tool_schemas()

    tools = []
    available_functions = {}

    for function in functions:
        tools.append({
            "type": "function",
            "function": {
                "name": function["name"],
                "description": function["description"],
                "parameters": function["parameters"],
                "return_type": function["return_type"],
            },
        })
        
        func_name = function["name"]
        available_functions[func_name] = get_tool_function(func_name)

    return tools, available_functions

class OpenAITooling:
    def __init__(
            self, 
            openai_api_key: str = None, 
            openai_model: str = None,
            tool_choice: str = "auto"):
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        self.tool_choice = tool_choice

    def get_api_key(self):
        """Handles OpenAI API tool calls."""
        return self.openai_api_key

    def call_tools(
            self,
            messages: list[dict[str, str]], 
            openai_api_key: str = get_api_key(), 
            openai_model: str = None,
            tool_choice: str = "auto") -> dict:

        messages.append({
            "role": "system",
            "content": f'''Choose one or multiple tools that would be useful for solving the task.'''
        })

        """Interprets a user query and returns a standardized response dict."""
        if openai_model is None:
            openai_model = self.openai_model
        if openai_api_key is None:
            openai_api_key = self.openai_api_key

        client = OpenAI(api_key=openai_api_key)

        tools, available_functions = get_tools()
        messages = messages

        completion = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        response = completion.choices[0].message
        tool_calls = response.tool_calls
        
        if tool_calls:
            for tool_call in tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                function_to_call = available_functions[name]
                
                # Tool functions now return standardized responses
                result = function_to_call(**args)
                messages.append({
                    "role": "function",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": result
                })

        return messages
openai = OpenAITooling()