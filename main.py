import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
try:
    api_key = os.getenv("GEMINI_API_KEY")
except KeyError:
    raise KeyError("API KEY not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


def call_model(messages):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )
    return response


def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        model_response = call_model(messages)
        if model_response.candidates:
            for candidate in model_response.candidates:
                messages.append(candidate.content)

        prompt_metadata = model_response.usage_metadata
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_metadata.prompt_token_count}")
            print(f"Response tokens: {prompt_metadata.candidates_token_count}")

        function_calls = model_response.function_calls
        function_results = []

        if function_calls:
            for function_call in function_calls:
                # print(f"Calling function: {function_call.name}({function_call.args})")
                if args.verbose:
                    function_call_result = call_function(function_call, True)
                else:
                    function_call_result = call_function(function_call)

                if not function_call_result.parts:
                    raise Exception("Error: No function parts returned")
                elif not function_call_result.parts[0].function_response:
                    raise Exception("Error: No function response returned")
                elif not function_call_result.parts[0].function_response.response:
                    raise Exception("Error: No result in function response")
                else:
                    function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

            messages.append(types.Content(role="user", parts=function_results))

        else:
            print(model_response.text)
            return

    print("Error: Maximum iterations reached without final response")
    exit(1)


if __name__ == "__main__":
    main()
