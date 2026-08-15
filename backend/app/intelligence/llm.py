"""One function to talk to a model. Swap providers with one line in .env

FREE OPTIONS, no credit card needed:
  gemini  - aistudio.google.com -> "Get API key". Best free tier. Start here.
  groq    - console.groq.com. Very fast, free, rate limited.
  mistral - console.mistral.ai. Free tier.
  ollama  - runs on your laptop, no key, works with no internet at all.

Everything else in this repo calls ask() and nothing else, so if a sponsor
hands you different credentials tomorrow, this is the only file you touch.
"""

import os
import json

from dotenv import load_dotenv
load_dotenv()  # read the .env file so `python llm.py` works on its own too

PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# Every provider below except Anthropic speaks the OpenAI protocol, so one
# client handles all of them. Only the base URL and model name change.
OPENAI_COMPATIBLE = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_env": "GEMINI_API_KEY",
        "model_env": "GEMINI_MODEL",
        "default_model": "gemini-flash-latest",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "model_env": "GROQ_MODEL",
        "default_model": "llama-3.3-70b-versatile",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "key_env": "MISTRAL_API_KEY",
        "model_env": "MISTRAL_MODEL",
        "default_model": "mistral-small-latest",
    },
    "openai": {
        "base_url": None,  # the library's own default
        "key_env": "OPENAI_API_KEY",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4o-mini",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": None,  # local, no key
        "model_env": "OLLAMA_MODEL",
        "default_model": "llama3.2",
    },
}


def ask(system: str, user: str, max_tokens: int = 2000) -> str:
    """Send a prompt, get text back. Raises on failure so errors are visible."""
    if PROVIDER == "anthropic":
        return _anthropic(system, user, max_tokens)
    if PROVIDER == "azure":
        return _azure(system, user, max_tokens)
    if PROVIDER in OPENAI_COMPATIBLE:
        return _openai_compatible(PROVIDER, system, user, max_tokens)
    raise ValueError(
        f"Unknown LLM_PROVIDER: {PROVIDER}. "
        f"Options: anthropic, azure, {', '.join(OPENAI_COMPATIBLE)}"
    )


def ask_json(system: str, user: str, max_tokens: int = 4000):
    """Same as ask(), but insists on JSON and parses it.

    Smaller free models wrap JSON in markdown fences even when told not to,
    and sometimes add a sentence before it. Strip both before parsing.
    """
    system = system + "\n\nRespond with valid JSON only. No preamble, no markdown fences."
    raw = ask(system, user, max_tokens).strip()

    if "```" in raw:
        parts = raw.split("```")
        if len(parts) > 1:
            raw = parts[1]
            if raw.lstrip().startswith("json"):
                raw = raw.lstrip()[4:]

    raw = raw.strip()

    # Last resort: grab the outermost array or object and ignore any chat around it.
    if not raw.startswith(("[", "{")):
        for opener, closer in (("[", "]"), ("{", "}")):
            start, end = raw.find(opener), raw.rfind(closer)
            if start != -1 and end > start:
                raw = raw[start:end + 1]
                break

    return json.loads(raw)


def _openai_compatible(name, system, user, max_tokens):
    from openai import OpenAI

    config = OPENAI_COMPATIBLE[name]
    api_key = os.environ[config["key_env"]] if config["key_env"] else "not-needed"

    kwargs = {"api_key": api_key}
    if config["base_url"]:
        kwargs["base_url"] = config["base_url"]

    client = OpenAI(**kwargs)
    model = os.getenv(config["model_env"], config["default_model"])

    resp = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content


def _anthropic(system, user, max_tokens):
    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def _azure(system, user, max_tokens):
    from openai import AzureOpenAI

    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )
    resp = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content


def provider_status() -> str:
    """Human-readable check for the sidebar, so a missing key is obvious at
    startup instead of at hour 12."""
    if PROVIDER == "anthropic":
        required = ["ANTHROPIC_API_KEY"]
    elif PROVIDER == "azure":
        required = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"]
    elif PROVIDER in OPENAI_COMPATIBLE:
        key_env = OPENAI_COMPATIBLE[PROVIDER]["key_env"]
        required = [key_env] if key_env else []
    else:
        return f"UNKNOWN PROVIDER: {PROVIDER}"

    missing = [key for key in required if not os.getenv(key)]
    if missing:
        return f"{PROVIDER}: MISSING {', '.join(missing)} in .env"
    return f"{PROVIDER}: ready"


def selftest() -> str:
    """Run `python llm.py` to prove your key works before the hackathon starts."""
    print(provider_status())
    # Give newer "thinking" models enough room to answer, or the reply comes back empty.
    reply = ask("Reply with exactly: OK", "Say OK", max_tokens=500)
    print(f"Model replied: {reply!r}")
    return reply


if __name__ == "__main__":
    selftest()
