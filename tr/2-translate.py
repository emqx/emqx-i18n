#!/usr/bin/env python3

import argparse
import os
import sys
import openai
from pathlib import Path
from typing import Optional

DEFAULT_MODEL = "gpt-5.3-codex"


def yellow(text: str) -> str:
    """Return text wrapped in ANSI yellow color codes"""
    return f"\033[33m{text}\033[0m"


def green(text: str) -> str:
    """Return text wrapped in ANSI green color codes"""
    return f"\033[32m{text}\033[0m"


def diff_file_path() -> Path:
    """Return the file path of the diff file"""
    return Path(__file__).parent.parent / "tmp" / "desc.diff.hocon"


def read_diff_file() -> str:
    """Read the diff file to be translated"""
    diff_path = diff_file_path()
    with open(diff_path, "r", encoding="utf-8") as f:
        return f.read()


def clean_output(text: str) -> str:
    """Remove markdown code block markers if present."""
    lines = text.split("\n")
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)


def resolve_model(cli_model: Optional[str]) -> str:
    """Resolve model from CLI flag, env var, then default."""
    return cli_model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL


def translate_content(content: str, api_key: str, model: str) -> str:
    """Translate content using OpenAI Responses API."""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a professional technical translator. "
                "Translate the user input into Chinese and return only the translated HOCON content. "
                "Do not add explanations or markdown code fences."
            ),
            input=content,
            temperature=0.3,
        )
        translated = (response.output_text or "").strip()
        if not translated:
            print(yellow("Error: empty response from OpenAI"), file=sys.stderr)
            return ""
        return clean_output(translated)
    except Exception as e:
        print(yellow(f"Error during translation: {e}"), file=sys.stderr)
        return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Translate tmp/desc.diff.hocon into tmp/desc.tr.hocon")
    parser.add_argument(
        "--model",
        help=(
            "OpenAI model to use. "
            "Precedence: --model > OPENAI_MODEL > default gpt-5.3-codex"
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    content = read_diff_file()
    if not content:
        return

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(yellow("Error: OPENAI_API_KEY environment variable is not set"), file=sys.stderr)
        sys.exit(1)

    model = resolve_model(args.model)

    # Read input file
    diff_path = diff_file_path()
    if not diff_path.exists():
        print(yellow(f"Error: {diff_path} does not exist"), file=sys.stderr)
        sys.exit(1)

    # Translate the content
    print(f"Translating content from {diff_path} with model {model} ...")
    translated_content = translate_content(content, api_key, model)
    if not translated_content:
        return

    # Write the translation to desc.tr.hocon
    tr_path = diff_path.with_name("desc.tr.hocon")
    try:
        with open(tr_path, "w", encoding="utf-8") as f:
            f.write(translated_content)
        print(green(f"Translation written to {tr_path}"))
    except Exception as e:
        print(yellow(f"Error writing translation: {e}"), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
