import math

def free_will_index(entropy_score, unique_actions, markov_confidence):

    if unique_actions <= 1:
        return 0

    entropy_normalized = entropy_score / math.log2(unique_actions)

    if markov_confidence is None:
        markov_confidence = 0

    fwi = entropy_normalized * (1 - markov_confidence)

    return round(fwi, 3)