
# MARK: - pytoolkit.py
#!/usr/bin/env python3
import argparse
def build_parser():
	parser = argparse.ArgumentParser(description="PyToolkit text utilities")
	sub = parser.add_subparsers(dest="command",required=True)
	analyze = sub.add_parser("analyze", help="Analyze a text file")
	analyze.add_argument("-f","--file", required=True, help="Input file")
	analyze.add_argument("-v", "--verbose", action="store_true")
	return parser

def analyze_file(path, verbose=False):
	with open(path, encoding="utf-8") as f:
		text = f.read()
	words = text.split()
	print(f"Words: {len(words)}")
	counter, by_prefix = word_stats(words)
	if verbose:
		print(f"Characters: {len(text)}")
		print(f"Top words: {counter.most_common(10)}")
		print(f"Words by prefix: {dict(by_prefix)}")

from collections import Counter, defaultdict
def word_stats(words):
    counter = Counter(w.lower().strip(".,!?") for w in words if w)
    by_prefix = defaultdict(list)
    for w in counter:
        by_prefix[w[:1]].append(w)
    return counter, by_prefix

def main():
	args = build_parser().parse_args()
	if args.command == "analyze":
		analyze_file(args.file, args.verbose)

if __name__ == "__main__":
	main()


