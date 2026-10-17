import json
import os
import argparse
import sys
from dotenv import load_dotenv
from openai import Client, OpenAI
from functions.index import available_functions, call_function
from prompts import system_prompt

def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    # api_key = os.environ.get("REQUESTY_API_KEY")
    if api_key is None: raise RuntimeError("LLM API key could not be loaded")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        # base_url="https://router.requesty.ai/v1",
        api_key=api_key,
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.prompt
        }
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            # model="nvidia/nemotron-3-ultra-550b-a55b",
            messages= messages,
            tools=available_functions,
            temperature=0.5
        )

        if response.usage is None: raise RuntimeError("Error in model response")

        response_message = response.choices[0].message
        messages.append(response_message)

        tool_calls = response_message.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                try:
                    result_message = call_function(tool_call, args.verbose)
                    if args.verbose:
                        print(f"-> {result_message['content']}")
                    messages.append(result_message)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print(response_message.content)
            return
    print(f"Could not produce a final response. Messages so far: {messages[1:]}")
    sys.exit(1)

if __name__ == "__main__":
    main()
