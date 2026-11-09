import argparse
from .stats import word_stats
from collections.abc import Iterator

def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    return parser

def read_lines(path: str) -> Iterator[str]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

    """Yield stripped lines from a text file."""
def analyze_file(path, verbose=False):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    print(f"Words: {len(words)}")
    counter, by_prefix = word_stats(words)
    text_lines = read_lines(path)
    if verbose:
        print(f"Lines: {sum(1 for _ in text_lines)}")
        print(f"Characters: {len(text)}")
        print(f"Top words: {counter.most_common(10)}")
        print(f"Words by prefix: {dict(by_prefix)}")



def main():
    args = build_parser().parse_args()
    if args.command == "analyze":
        analyze_file(args.file, args.verbose)


if __name__ == "__main__":
    main()





 