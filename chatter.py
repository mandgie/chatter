import configparser
import time
from prompt_toolkit import PromptSession
import openai
from openai.error import RateLimitError
from rich import print as rprint
import typer
from typing import Optional, List
from dotenv import load_dotenv
import os

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
    session = PromptSession()
    return session.prompt(question)

def is_user_satisfied():
    while True:
        response = prompt_user("Are you satisfied with the answer? (yes/no): ").lower()
        if response in ["yes", "no"]:
            return response == "yes"
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_response(messages, model_name=model_name):
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
                raise typer.Abort()

def read_file_content(file_path: str):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        raise typer.Abort()

@app.command()
def ask(file_path: List[str] = typer.Option((), help="One or more file paths to provide as context"), 
        model: str = typer.Option(None, help="Name of the GPT model to use"),
        context_string: str = typer.Option('', help="A string to provide as context")):
    messages = []
    satisfied = False
    file_contents = []

    for file in file_path:
        file = os.path.abspath(file)
        file_name = os.path.basename(file)
        file_content = read_file_content(file)
        file_contents.append((file_name, file_content))

    while not satisfied:
        question = prompt_user("Please enter your question: ")

        for file_name, file_content in file_contents:
            question += f"\n{file_name}: \n{file_content}"

        if context_string:
            question += f"\nContext: \n{context_string}"

        messages.append({"role": "user", "content": question})

        if model:
            response = get_response(messages, model)
        else:
            response = get_response(messages)

        answer = response['choices'][0]['message']['content']
        rprint("[bold green]ASSISTANT:[/bold green]")
        rprint(answer)

        messages.append({"role": "assistant", "content": answer})

        satisfied = is_user_satisfied()

def main():
    app()

if __name__ == "__main__":
    main()
