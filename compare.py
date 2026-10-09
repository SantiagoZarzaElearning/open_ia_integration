"""Compare the same prompt at different temperatures."""

import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_PROMPT = "Explain what a token is in one short paragraph."


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Compare model outputs across temperatures.")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--temperatures", type=float, nargs="+", default=[0.0, 0.7, 1.5])
    parser.add_argument("--max-tokens", type=int, default=300)
    parser.add_argument("--system", default=os.getenv("OPENAI_SYSTEM", "You are a helpful assistant."))
    return parser.parse_args(argv)


def main(argv=None):
    load_dotenv()
    args = parse_args(argv)
    if not os.getenv("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY. See .env.example.", file=sys.stderr)
        raise SystemExit(1)
    client = OpenAI()

    print(f"Prompt: {args.prompt}\n")
    for temp in args.temperatures:
        try:
            response = client.chat.completions.create(
                model=args.model,
                messages=[
                    {"role": "system", "content": args.system},
                    {"role": "user", "content": args.prompt},
                ],
                temperature=temp,
                max_tokens=args.max_tokens,
            )
            text = response.choices[0].message.content
        except Exception as exc:
            print(f"--- temperature={temp} ---\nAPI error: {exc}\n", file=sys.stderr)
            continue
        print(f"--- temperature={temp} ---\n{text}\n")


if __name__ == "__main__":
    main()
