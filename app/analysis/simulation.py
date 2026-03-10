import random
from collections import Counter, defaultdict
from typing import List
from app.analysis.markov import build_transition_matrix, normalize_transitions
from app.models import DecisionEvent
from app.schema import get_time_bucket

def simulate_future(events: List[DecisionEvent], steps: int = 10):

    if len(events) < 2:
        return []

    transitions = build_transition_matrix(events)
    probabilities = normalize_transitions(transitions)

    current_action = events[-1].action

    simulated = []

    for _ in range(steps):

        if current_action not in probabilities:
            break

        actions = list(probabilities[current_action].keys())
        probs = list(probabilities[current_action].values())

        next_action = random.choices(actions, probs)[0]

        simulated.append(next_action)

        current_action = next_action

    return simulated

def find_dominant_loop(sequence):

    if not sequence:
        return []

    pairs = [(sequence[i], sequence[i+1]) for i in range(len(sequence)-1)]

    counter = Counter(pairs)

    most_common = counter.most_common(1)

    if not most_common:
        return []

    return list(most_common[0][0])

def simulated_predictability(sequence):

    if not sequence:
        return None

    counts = Counter(sequence)

    dominant = max(counts.values())

    return round(dominant / len(sequence), 2)