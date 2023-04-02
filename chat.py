"""
1. `pip install openai`
2. Get OPENAI_API_KEY from https://platform.openai.com/account/api-keys
3. Set environment variable OPENAI_API_KEY
4. [Optional] In shell, `alias chat="OPENAI_API_KEY=$OPENAI_API_KEY python chat.py"`
"""

import os
import openai
import shutil
import getpass
import json
from datetime import datetime

LOG_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/logs"
CURRENT_DATE = datetime.utcnow().strftime('%Y-%m-%d')

try:
    os.mkdir(LOG_DIR)
except FileExistsError:
    pass

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = "org-7Tk4iNWIE2oAehANpliVvSpP"

USER = getpass.getuser()
INITIAL_CONTENT = {"role": "system", "content": "You are a helpful assistant."}
MAX_CHAT_LENGTH = 20


def _log(current_context):
    with open(f"{LOG_DIR}/{CURRENT_DATE}.json", 'a') as f:
        f.write("Session:")
        for each in current_context:
            f.write(json.dumps(each))
        f.write("\n\n")


def main():
    current_context = []

    try:
        while True:
            if not current_context:
                print(
                    f"Starting new session (the maximum session length is {MAX_CHAT_LENGTH})..."
                )
                current_context.append(INITIAL_CONTENT)

            print(f"[{USER}]: ", end="")
            question = input()
            current_context.append({
                "role": "user",
                "content": question,
            })
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=current_context,
            )
            role = response["choices"][0]["message"]["role"]
            content = response["choices"][0]["message"]["content"]
            current_context.append({
                "role": role,
                "content": content,
            })
            print(f"[ChatGPT]: {content}")

            columns, _ = shutil.get_terminal_size()
            print("-" * columns)

            if len(current_context) > MAX_CHAT_LENGTH:
                print(
                    f"Current context is too long, reset chat to reduce response"
                )
                _log(current_context)
                current_context = []
    except KeyboardInterrupt:
        _log(current_context)


main()
