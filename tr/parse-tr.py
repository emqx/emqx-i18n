#! /usr/bin/env python3

# This script takes the translation result file as input,
# parse the lines, and print out the lines which can be concatenated
# to the current desc.zh.hocon file.

import sys
import os.path

if len(sys.argv) < 2:
    tr_file = "tmp/desc.tr.hocon"
else:
    tr_file = sys.argv[1]

if not os.path.exists(tr_file):
    print("Error: {} does not exist".format(tr_file), file=sys.stderr)
    sys.exit(1)

untranslated_keys = []
with open(tr_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            continue
        if len(line) == 0:
            continue
        if '=' not in line:
            print("Error: {} is not a valid line".format(line), file=sys.stderr)
            sys.exit(1)
        key, value = [x.strip() for x in line.split('=', 1)]
        if key.endswith('.en'):
            continue
        if 'NEED_TRANSLATION' in value:
            untranslated_keys.append(key)
        print(f"{key.replace('.zh', '')} = {value}")

if untranslated_keys:
    print("Error: Found untranslated text", file=sys.stderr)
    for key in untranslated_keys:
        print(key, file=sys.stderr)
    sys.exit(1)
