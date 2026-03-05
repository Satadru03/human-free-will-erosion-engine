import math
from collections import Counter

import math
from collections import Counter
from typing import List
from app.models import DecisionEvent

from datetime import timedelta

def calculate_entropy(events: List[DecisionEvent]) -> float:

    if not events:
        return 0.0

    actions = [event.action for event in events]

    counts = Counter(actions)

    total = len(actions)

    entropy = 0.0

    for count in counts.values():

        p = count / total

        entropy -= p * math.log2(p)

    return round(entropy, 3)

def rolling_entropy(events: List[DecisionEvent]):

    daily_entropy = {}

    events_by_day = {}

    for event in events:

        day = event.occurred_at.date()

        events_by_day.setdefault(day, []).append(event)

    for day, day_events in events_by_day.items():

        daily_entropy[day] = calculate_entropy(day_events)

    return daily_entropy