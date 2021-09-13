import random
import bisect
from django.db.models import Sum
from markovify import Chain
from markovify.chain import accumulate
from .models import MarkovChainState3

class SQLChainState3(Chain):
    state_size = 3
    def __init__(self, user_ids):
        self.user_ids = user_ids

    def move(self, state):
        next_and_value = MarkovChainState3.objects.filter(user_id__in=self.user_ids).filter(state0=state[0], state1=state[1], state2=state[2]).values_list("next").annotate(value=Sum("value"))
        choices, weights = zip(*next_and_value)
        cumdist = list(accumulate(weights))
        r = random.random() * cumdist[-1]
        selection = choices[bisect.bisect(cumdist, r)]
        return selection
