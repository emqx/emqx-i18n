#!/usr/bin/env python3

import os
import sys
import openai
from pathlib import Path
import time
from typing import List

def yellow(text: str) -> str:
    """Return text wrapped in ANSI yellow color codes"""
    return f"\033[33m{text}\033[0m"

def green(text: str) -> str:
    """Return text wrapped in ANSI green color codes"""
    return f"\033[32m{text}\033[0m"

def diff_file_path() -> str:
    """Return the file path of the diff file"""
    return Path(__file__).parent.parent / "tmp" / "desc.diff.hocon"

def read_diff_file() -> str:
    """Read the diff file to be translated"""
    diff_path = diff_file_path()
    with open(diff_path, "r", encoding="utf-8") as f:
        return f.read()

def translate_content(content: str) -> str:
    """Translate content using ChatGPT"""
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional technical translator."},
                {"role": "user", "content": content}
            ],
            temperature=0.3
        )
        translated = response.choices[0].message.content
        # Remove markdown code block markers if present
        lines = translated.split('\n')
        if lines and lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].startswith('```'):
            lines = lines[:-1]
        return '\n'.join(lines)
    except Exception as e:
        print(yellow(f"Error during translation: {e}"), file=sys.stderr)
        return ""

def main():
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(yellow("Error: OPENAI_API_KEY environment variable is not set"), file=sys.stderr)
        return

    openai.api_key = api_key

    # Read input file
    diff_path = diff_file_path()
    if not diff_path.exists():
        print(yellow(f"Error: {diff_path} does not exist"), file=sys.stderr)
        return

    content = read_diff_file()
    if not content:
        return

    # Translate the content
    print(f"Translating content from {diff_path} ...")
    translated_content = translate_content(content)
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

if __name__ == "__main__":
    main()
