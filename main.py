import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Api key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
i = 0

for _ in range(20):
    i += 1
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions]
            )
        )
    
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if response.usage_metadata != None:
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens: ", response.usage_metadata.candidates_token_count)

    if response.function_calls:
        function_result_list = []

        function_calls = response.function_calls
        for function_call in function_calls:
            function_call_result = call_function(function_call)

            if not function_call_result.parts:
                raise Exception(f"Error: Function call {function_call} resulted in empty parts list")
            
            if function_call_result.parts[0].function_response is None:
                raise Exception("Error: Function response was None")
            
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Error: Function response.response is None")
            
            function_result_list.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_result_list))
        
    else:
        print(response.text)
        break

if i == 20:
    print("Maximum number of iterations reached.")
    exit(1)