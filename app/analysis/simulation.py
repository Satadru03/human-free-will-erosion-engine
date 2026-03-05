import random
from typing import List, Dict

from app.models import DecisionEvent
from app.analysis.markov import build_transition_matrix, normalize_transitions


def simulate_future(events: List[DecisionEvent], steps: int = 10) -> List[str]:

    if len(events) < 2:
        return []

    transitions = build_transition_matrix(events)
    probabilities = normalize_transitions(transitions)

    current_action = events[-1].action

    simulated = []

    for _ in range(steps):

        if current_action not in probabilities:
            break

        next_actions = probabilities[current_action]

        actions = list(next_actions.keys())
        weights = list(next_actions.values())

        next_action = random.choices(actions, weights=weights)[0]

        simulated.append(next_action)

        current_action = next_action

    return simulated