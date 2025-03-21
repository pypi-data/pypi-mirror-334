import json
from openai import OpenAI
from tool import get_tools

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
        return self.openai_api_key

    """Handles OpenAI API tool calls."""
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