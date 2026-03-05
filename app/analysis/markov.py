from collections import defaultdict
from typing import List, Tuple
from app.models import DecisionEvent

def build_transition_matrix(events: List[DecisionEvent]):

    transitions = defaultdict(lambda: defaultdict(int))

    for i in range(len(events) - 1):

        current_action = events[i].action
        next_action = events[i + 1].action

        transitions[current_action][next_action] += 1

    return transitions

def normalize_transitions(transitions):

    probabilities = {}

    for current_action, next_actions in transitions.items():

        total = sum(next_actions.values())

        probabilities[current_action] = {
            action: count / total
            for action, count in next_actions.items()
        }

    return probabilities

def predict_next_action(events: List[DecisionEvent]) -> Tuple[str | None, float | None]:

    if len(events) < 2:
        return None, None

    transitions = build_transition_matrix(events)

    probabilities = normalize_transitions(transitions)

    last_action = events[-1].action

    if last_action not in probabilities:
        return None, None

    next_action = max(probabilities[last_action], key=probabilities[last_action].get)

    confidence = probabilities[last_action][next_action]

    return next_action, round(confidence, 2)