#!/usr/bin/env python3

import sys
from pathlib import Path

def yellow(text: str) -> str:
    """Return text wrapped in ANSI yellow color codes"""
    return f"\033[33m{text}\033[0m"

def parse_line(line):
    # Parse line in format: docid = "doc text"
    line = line.strip()
    pos = line.find('=')
    if pos == -1:
        return None, None

    docid = line[:pos].strip()
    content = line[pos+1:].strip()

    # Check for and remove surrounding quotes
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]

    return docid, content

def load_translations(filename):
    translations = {}
    with open(filename, 'r') as f:
        for line in f:
            docid, text = parse_line(line)
            if docid:
                translations[docid] = text
    return translations

def main():
    if len(sys.argv) != 5:
        print("Usage: {} source_file target_file base_file compare_base".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]
    base_file = sys.argv[3]
    compare_base = sys.argv[4]

    # Load target translations
    target_translations = load_translations(target_file)

    # Load base translations
    if compare_base == "none":
        base_docs = {}
    else:
        base_docs = load_translations(base_file)

    # Process source file and collect output lines
    output_lines = []
    with open(source_file, 'r') as f:
        for line in f:
            docid, text = parse_line(line)
            if docid:
                source_text = text
                target_text = target_translations.get(docid, "NEED_TRANSLATION")
                if target_text == "----":
                    target_text = "NEED_TRANSLATION"
                base_text = base_docs.get(docid)
                if base_text and base_text != source_text:
                    output_lines.extend([
                        f'#NEED_TRANSLATION: CHANGED_SINCE {compare_base}',
                        f'#{docid}.en = "{base_text}"',
                        f'{docid}.en = "{source_text}"',
                        f'{docid}.zh = "{target_text}"',
                        ''  # Empty line for separation
                    ])
                elif target_text == "NEED_TRANSLATION":
                    output_lines.extend([
                        f'{docid}.en = "{source_text}"',
                        f'{docid}.zh = "NEED_TRANSLATION"',
                        ''  # Empty line for separation
                    ])

    # Check if any lines were collected
    if not output_lines:
        print(yellow("No lines were collected for translation"), file=sys.stderr)
        # do not fail, just return
        return

    # Print prompt.hocon content first
    prompt_path = Path(__file__).parent / "prompt.hocon"
    if prompt_path.exists():
        with open(prompt_path, 'r', encoding='utf-8') as f:
            print(f.read().strip())
            print()  # Add a blank line after prompt

    # Print all collected lines
    print('\n'.join(output_lines))

if __name__ == "__main__":
    main()
