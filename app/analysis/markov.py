from collections import defaultdict

def predict_next_action(actions):

    transitions = defaultdict(lambda: defaultdict(int))

    for i in range(len(actions)-1):
        a = actions[i]
        b = actions[i+1]
        transitions[a][b] += 1

    return transitions