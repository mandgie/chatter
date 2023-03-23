# chatter
A python chatGPT cli built with Typer
# Chatter

Chatter is a simple command-line tool that allows you to have a conversation using any of OpenAI's CHAT-GPT models. It also supports reading additional context from a given file to help with generating accurate answers.

## Requirements

- Python 3.9+
- Typer
- OpenAI
- python-dotenv

## Installation

1. Make sure you have Python 3.9+ installed on your system.

2. Clone the repository. You can do so by running the following command:

   ```
   git clone git@github.com:mandgie/chatter.git
   ```

3. Create a virtual environment and activate it:

   Example using venv:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```


5. Create a `.env` file in the same directory as the script and set your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

6. Modify the config file by choosing model and path to your python executable. The default config file is located at `config.ini`.

## Usage

To use Chatter, simply run the script using the following command:

```
python chatter.py
```

After running the script, you'll be prompted to ask your question. If you want to provide additional context from a file, you can do so by providing the file path (absolute or relative) as a parameter, like this:

```
python chatter.py --file_path path/to/your/context_file.txt
```

Once you've asked a question, the script will return an answer from GPT. You can continue asking questions until you're satisfied with the answer.

To exit the script, simply input "yes" when asked if you're satisfied with the answer, or press `CTRL+C`.

### Setting up a symlink on macOS

To create a symlink to execute the CLI with the word "chatter" on macOS, follow the steps below:

1. Run the following command to create a symlink called "chatter":

   ```
   ln -s ./launcher.sh /usr/local/bin/chatter
   ```

2. Now you can start the CLI anywhere by using the word "chatter".

   ```
   chatter
   ```

## Troubleshooting

If you encounter any rate-limiting issues, the script will automatically retry until the maximum number of retries is reached (default is 5). If the maximum number of retries is reached, the script will exit with an error message.

## Contributing
Thank you for considering contributing to this project! I appreciate any help and suggestions that can make this tool even better. If you would like to contribute, here are a few guidelines:

1. Fork the repository on GitHub and clone your fork to your local machine.
2. Create a new branch for your feature or bugfix.
3. Commit your changes to the new branch, following the commit message guidelines.
4. Push your changes to your fork.
5. Create a pull request, describing the changes and their purpose.