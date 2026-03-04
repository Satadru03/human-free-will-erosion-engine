import math
from collections import Counter

def decision_entropy(actions: list[str]) -> float:
    total = len(actions)

    if total == 0:
        return 0

    counts = Counter(actions)

    entropy = 0

    for c in counts.values():
        p = c / total
        entropy -= p * math.log2(p)

    return entropy