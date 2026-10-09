# open_ia_integration

Project URL: https://github.com/SantiagoZarzaElearning/open_ia_integration

Call OpenAI models directly from Python instead of using the browser chat. Experiment with `system` message, `temperature`, and `max_tokens`.

## Setup

1. Create an account and an API key: https://platform.openai.com/api-keys
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Store the key as an environment variable (never commit it):

```bash
copy .env.example .env
```

then edit `.env` and set `OPENAI_API_KEY=sk-...`

## Usage

Interactive chat (user input -> model response):

```bash
python chat.py
python chat.py --model gpt-4o-mini --temperature 0.7 --max-tokens 500 --system "You are a helpful assistant."
```

Compare outputs at different temperatures:

```bash
python compare.py
python compare.py --prompt "Explain what a token is" --temperatures 0.0 0.7 1.5
```

## What you learn

- `client.chat.completions.create()` (current `openai>=1.0.0` syntax: `from openai import OpenAI; client = OpenAI()`)
- `temperature` controls randomness, `max_tokens` limits response length, `system` sets model behavior.
- What tokens are, by observing length/cost effects of `max_tokens`.

Note: a 2023 Towards Data Science walkthrough of this project uses the legacy `openai.ChatCompletion.create()` syntax (deprecated late 2023). Concepts still apply; this repo uses the updated client syntax.
