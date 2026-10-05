from collections import Counter, defaultdict
def word_stats(words):
    counter = Counter(w.lower().strip(".,!?") for w in words if w)
    by_prefix = defaultdict(list)
    for w in counter:
        by_prefix[w[:]].append(w)
    return counter, by_prefix