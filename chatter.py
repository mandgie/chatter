import configparser
import time
import openai
from openai.error import RateLimitError
import typer
from dotenv import load_dotenv
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
dotenv_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path)

config = configparser.ConfigParser()
config_path = os.path.join(script_dir, "config.ini")
config.read(config_path)

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = typer.Typer()

# Replace the hardcoded model name with its value from the config file
model_name = config.get("general", "default_model")

def prompt_user(question: str):
    return input(question)

def is_user_satisfied():
    while True:
        response = prompt_user("Are you satisfied with the answer? (yes/no): ").lower()
        if response in ["yes", "no"]:
            return response == "yes"
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_response(messages):
    max_retries = 5
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            return openai.ChatCompletion.create(
                model=model_name,
                messages=messages
            ) 
        except RateLimitError:
            if attempt < max_retries - 1:
                print(f"Rate limit exceeded, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("Max retries reached. Exiting.")
                raise

def read_file_content(file_path: str):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

@app.command()
def ask(file_path: str = None):
    messages = []
    satisfied = False

    while not satisfied:
        question = prompt_user("Please enter your question: ")

        if file_path:
            # Convert the relative path to an absolute path if provided
            file_path = os.path.abspath(file_path)
            file_content = read_file_content(file_path)
            if file_content:
                question += f"\n {file_content}"

        messages.append({"role": "user", "content": question})

        response = get_response(messages)

        answer = response['choices'][0]['message']['content']
        typer.echo(answer)

        messages.append({"role": "assistant", "content": answer})

        satisfied = is_user_satisfied()

def main():
    app()

if __name__ == "__main__":
    main()