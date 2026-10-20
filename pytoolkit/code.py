
# MARK: - PyToolkit_content.py
# MARK: - __init__.py

#!/usr/bin/env python3

import argparse
import io
from collections import Counter, defaultdict
from contextlib import redirect_stdout
import sys
from functools import lru_cache, partial, update_wrapper, wraps
import importlib
from itertools import groupby, combinations
def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@lru_cache(maxsize=32)
def cached_world_count(text):
    return len(text.split())

# MARK: - cli.py
def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    return parser

# MARK: - uppercase.py
def apply(text):
    return text.upper()

def load_plugin(uppercase):
    module = importlib.import_module(f"pytoolkit.plugins.{uppercase}")
    return module.apply

def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

def count_lines(path):
    return sum(1 for _ in read_lines (path))

def prefix_groups_groups(words):
    for prefix, group in groupby(sorted(words), key=lambda w: w[0]):
        yield prefix, list(group)

def word_pairs(words, n=2):
    return list(combinations(words[:6], n))

def analyze_file(path, verbose=False):
    with open(path, encoding="utf-8") as f:
        text = load_plugin("uppercase")(f.read())
    words = text.split()
    line_count = count_lines(path)
    print(f"Words: {len(words)}")
    word_counter, by_prefix = word_stats(words)
    Group_by_prefix = list(prefix_groups_groups(word_counter))
    pair_words = list(word_pairs(words))
    if verbose:
        print(f"Line count: {line_count}")
        print(f"Characters: {len(text)}")
        print(f"Top words: {word_counter.most_common(10)}")
        print(f"Words by prefix: {dict(by_prefix)}")
        print(f"Group by prefix: {Group_by_prefix}")
        print(f"Pair word: {pair_words}")
analyze_short = partial(analyze_file, verbose=False)

# MARK: - stats.py
def word_stats(words):
    word_counter = Counter(w.strip(".,!?") for w in words if w)
    by_prefix = defaultdict(list)
    for w in word_counter:
        by_prefix[w[0]].append(w)
    return word_counter, by_prefix


def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return None


def capture_report(path):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")
    return buffer.getvalue()



def main():
    args = build_parser().parse_args()
    if args.command == "analyze":
        text = safe_read(args.file)
    
        if text is None:
            sys.exit(1)

        analyze = log_call(analyze_short )
        update_wrapper(analyze, analyze_short )
        result1 = cached_world_count(text)
        result2 = cached_world_count(text)

        print(result1)
        print(result2)
        print(cached_world_count.cache_info())
        print(capture_report(args.file), end="")
        analyze_file(args.file, args.verbose)


if __name__ == "__main__":
    main()



