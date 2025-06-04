from typing import List, Dict
from litellm import completion
from dotenv import load_dotenv
'''
About this code:
This program is a simple example of using the litellm Python library to interact with a Large Language Model (LLM) — specifically, Anthropic’s Claude 3 model
'''


load_dotenv()

'''
litellm is a lightweight Python library designed to make it easy to interact with various large language models (LLMs) through a simple and unified interface.
completion is typically a function that sends a prompt or conversation history to a Large Language Model (LLM) and returns the generated text response (called a completion).
'''
def generate_response(messages: List[Dict]) -> str:

    response = completion(
        model="anthropic/claude-3-opus-20240229",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


'''
Set up the messages:
A "system" message that sets the context (an expert software engineer favoring functional programming).
It Sets the behavior, context, or instructions for the assistant.
It’s like the "director" telling the AI how to behave.
Usually only one system message at the start.

A "user" message requesting a function to swap keys and values in a dictionary.
Its the user’s input, questions, or commands.
This is what the human wants the AI to respond to.
'''
messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)