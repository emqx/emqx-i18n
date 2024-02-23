#!/usr/bin/env python3

"""
This script is used to compare and merge two JSON files. It provides four commands:

1. diff: Find the fields that are in the source file but not in the target file.
    Usage: python3 tools.py diff [SOURCE] [TARGET]

2. diff_content: Find the fields that are in the source file but have different content in the target file.
    Usage: python3 tools.py diff_content [SOURCE] [TARGET]

2. untranslated/UT: Find the fields that have not been translated in the source file.
    Usage: python3 tools.py untranslated [SOURCE] [--dict DICT]

3. merge: Merge the fields from the target file into the source file.
    Usage: python3 tools.py merge [SOURCE] [TARGET]

The dictionary file for the 'untranslated' command can be provided with the --dict option.
"""

import json
import argparse
import re
from collections.abc import Mapping

# Function to load a JSON file


def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: File {file_path} is not a valid JSON file.")
        raise

# Function to load a dictionary file


def load_dict(dict_file):
    with open(dict_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

# Depth-First Search to find differences between two JSON objects


def dfs(path, obj_a, obj_b, result):
    if isinstance(obj_a, Mapping):
        for key in obj_a:
            if obj_b is None or key not in obj_b:  # If key is not in obj_b, add it to result
                # Convert list to string to avoid TypeError
                nested_result = result
                for sub_key in path:
                    if sub_key not in nested_result:
                        nested_result[sub_key] = {}
                    nested_result = nested_result[sub_key]
                nested_result[key] = obj_a[key]
            else:
                # Recursively check for nested fields
                dfs(path + [key], obj_a[key], obj_b[key], result)
    return result


# Function to find fields that are in source but not in target


def find_diff(source, target):
    obj_a = load_json(source)
    obj_b = load_json(target)
    result = dfs([], obj_a, obj_b, {})
    print(json.dumps(result, indent=2, ensure_ascii=False))

# Function to check if a string contains Chinese characters


def contains_chinese(s):
    if not s.strip():  # Check if the string is empty or only contains spaces
        return True
    return any(u'\u4e00' <= c <= u'\u9fff' for c in s)

# Function to find fields that have not been translated

# Function to find differences between two JSON objects
def dfs_content_diff(path, obj_a, obj_b, result):
    if isinstance(obj_a, Mapping):
        for key in obj_a:
            if key in obj_b:  # If key is in both obj_a and obj_b
                if isinstance(obj_a[key], Mapping) and isinstance(obj_b[key], Mapping):
                    # Recursively check for nested fields
                    new_result = {}
                    dfs_content_diff(path + [key], obj_a[key], obj_b[key], new_result)
                    if new_result:
                        nested_result = result
                        for sub_key in path:
                            if sub_key not in nested_result:
                                nested_result[sub_key] = {}
                            nested_result = nested_result[sub_key]
                        nested_result[key] = new_result
                elif obj_a[key] != obj_b[key]:  # If the values are not equal, add it to result
                    nested_result = result
                    for sub_key in path:
                        if sub_key not in nested_result:
                            nested_result[sub_key] = {}
                        nested_result = nested_result[sub_key]
                    nested_result[key] = obj_a[key]
                    nested_result[f"{key}_new"] = obj_b[key]
    return result

# Function to find content differences between source and target
def find_content_diff(source, target):
    obj_a = load_json(source)
    obj_b = load_json(target)
    result = dfs_content_diff([], obj_a, obj_b, {})
    print(json.dumps(result, indent=2, ensure_ascii=False))

def find_untranslated(source, dict_file=None):
    obj_a = load_json(source)
    dict_set = load_dict(dict_file) if dict_file else None

    def dfs_untranslated(path, obj):
        if isinstance(obj, str):
            if not contains_chinese(obj) and (not dict_set or obj not in dict_set):
                return obj
            return None
        elif isinstance(obj, Mapping):
            new_obj = type(obj)()  # Create a new object of the same type
            for key, value in obj.items():
                new_value = dfs_untranslated(path + [key], value)
                if new_value is not None:  # Only keep the field if it has not been translated
                    new_obj[key] = new_value
            return new_obj if new_obj else None  # Return None if the new object is empty

    result = dfs_untranslated([], obj_a)
    # ensure_ascii=False to print unicode characters
    print(json.dumps(result, indent=2, ensure_ascii=False))

# Function to merge fields from a third file into source
# Function to merge fields from a third file into source


def merge_fields(source, target):
    obj_a = load_json(source)
    obj_b = load_json(target)

    def dfs_merge(obj_a, obj_b):
        for key in obj_b:
            if key in obj_a and isinstance(obj_a[key], Mapping) and isinstance(obj_b[key], Mapping):
                dfs_merge(obj_a[key], obj_b[key])
            else:
                obj_a[key] = obj_b[key]

    dfs_merge(obj_a, obj_b)
    # ensure_ascii=False to print unicode characters
    print(json.dumps(obj_a, indent=2, ensure_ascii=False))


# Main function to parse command line arguments and call the appropriate function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['diff', 'diff_content', 'untranslated', 'UT', 'merge'])
    parser.add_argument("source", nargs='?', default=None)
    # Make target optional
    parser.add_argument("target", nargs='?', default=None)
    parser.add_argument(
        "--dict", default='scripts/no-translate-dict.txt', help="The path to the dictionary file (optional).")
    args = parser.parse_args()

    if args.command == 'diff':
        if args.source is None:
            args.source = 'desc.en.hocon'
        if args.target is None:
            args.target = 'desc.zh.hocon'
        find_diff(args.source, args.target)
    elif args.command == 'diff_content':
        if args.source is None:
            args.source = 'desc.en.hocon'
        if args.target is None:
            args.target = 'desc.zh.hocon'
        find_content_diff(args.source, args.target)
    elif args.command == 'untranslated' or args.command == 'UT':
        if args.source is None:
            args.source = 'desc.zh.hocon'
        find_untranslated(args.source, args.dict)
    elif args.command == 'merge':
        if args.source is None:
            args.source = 'desc.zh.hocon'
        if args.target is None:
            print("Please provide a target file for 'merge' command")
        elif args.target == 'desc.zh.hocon' or args.target == 'desc.en.hocon':
            print("Please do not use 'desc.*.hocon' as the target file, merge file should be a diff or untranslated output file")
        else:
            merge_fields(args.source, args.target)
