# chai

Chat with AI in the terminal.

**`chai` supports the following providers:**
- Anthropic (Claude)
- Google (Gemini)
- Mistral (Le Chat)
- OpenAI (ChatGPT)
- xAI (Grok)

**Why `chai` vs official apps and websites?**
- No usage limits (pay-as-you-go).
- Less expensive than subscriptions for light use.
- No login required after setting API key(s).
- One interface for multiple providers, models.
- More private: all chat history is stored locally.

**Why `chai` vs local LLMs (e.g., `ollama`)?**
- Access leading, state of the art models.
- No need to download models.
- No need to buy hardware.

## Installation

```sh
pip install chai-chat
```

## Usage

```sh
chai -h
```

Use `/?` or `/help` to print available commands.

Set your API key(s):

```sh
# Anthropic
export ANTHROPIC_API_KEY='your-anthropic-api-key'

# Google
export GOOGLE_API_KEY='your-google-api-key'

# Mistral
export MISTRAL_API_KEY='your-mistral-api-key'

# OpenAI
export OPENAI_API_KEY='your-openai-api-key'

# xAI
export XAI_API_KEY='your-xai-api-key'
```

## Development

1. [Install or update `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

2. Run `chai.py`:
   ```sh
   uv run chai.py -h
   ```
