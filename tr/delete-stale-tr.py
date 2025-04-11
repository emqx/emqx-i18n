#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Set

def yellow(text: str) -> str:
    """Return text wrapped in ANSI yellow color codes"""
    return f"\033[33m{text}\033[0m"

def green(text: str) -> str:
    """Return text wrapped in ANSI green color codes"""
    return f"\033[32m{text}\033[0m"

def extract_keys(file_path: str) -> Set[str]:
    """Extract keys from a HOCON file"""
    keys = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key = line.split('=')[0].strip()
            if key:
                keys.add(key)
    return keys

def filter_zh_file(en_keys: Set[str], zh_file: str) -> None:
    """Filter zh file to keep only keys that exist in en file"""
    with open(zh_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Track deleted keys for reporting
    deleted_keys = set()
    kept_lines = []

    for line in lines:
        line = line.rstrip()
        if not line or line.startswith('#'):
            kept_lines.append(line)
            continue

        if '=' in line:
            key = line.split('=')[0].strip()
            if key in en_keys:
                kept_lines.append(line)
            else:
                deleted_keys.add(key)

    # Print the filtered content
    print('\n'.join(kept_lines))

    # Report deleted keys
    if deleted_keys:
        print(yellow(f"\nDeleted {len(deleted_keys)} keys not found in English file:"), file=sys.stderr)
        for key in sorted(deleted_keys):
            print(yellow(f"  - {key}"), file=sys.stderr)
    else:
        print(green("\nNo keys were deleted"), file=sys.stderr)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <en_file> <zh_file>", file=sys.stderr)
        sys.exit(1)

    en_file = sys.argv[1]
    zh_file = sys.argv[2]

    # Extract keys from English file
    en_keys = extract_keys(en_file)
    print(green(f"Found {len(en_keys)} keys in English file"), file=sys.stderr)

    # Filter Chinese file
    filter_zh_file(en_keys, zh_file)

if __name__ == "__main__":
    main()
