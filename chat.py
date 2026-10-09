"""Interactive chat with OpenAI models (current client syntax, openai>=1.0.0)."""

import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_SYSTEM = "You are a helpful assistant."


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Chat with an OpenAI model from the terminal.")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=500)
    parser.add_argument("--system", default=os.getenv("OPENAI_SYSTEM", DEFAULT_SYSTEM))
    return parser.parse_args(argv)


def check_api_key():
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "Missing OPENAI_API_KEY. Set it as an environment variable or in a .env file.\n"
            "See .env.example. Get a key at https://platform.openai.com/api-keys",
            file=sys.stderr,
        )
        raise SystemExit(1)


def ask(client, model, system, temperature, max_tokens, user_message):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def main(argv=None):
    load_dotenv()
    args = parse_args(argv)
    check_api_key()
    client = OpenAI()

    print(f"Model: {args.model} | temperature: {args.temperature} | max_tokens: {args.max_tokens}")
    print(f"System: {args.system}")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        if not user_input:
            continue
        try:
            reply = ask(client, args.model, args.system, args.temperature, args.max_tokens, user_input)
        except Exception as exc:
            print(f"API error: {exc}", file=sys.stderr)
            continue
        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    main()
