from collections import MutableMapping
from functools import wraps

from pymachine.condition import Condition
from pymachine.exceptions import (
    UnknownInput,
    DuplicateCondition,
)


class TransitionTable(MutableMapping):
    def __init__(self):
        self.__table = {}

    def __setitem__(self, key, value):
        self.__table[key] = value

    def __delitem__(self, key):
        del self.__table[key]

    def __getitem__(self, condition):
        transition = self.__table.get(condition)
        if not transition:
            raise UnknownInput(condition)
        return transition

    def __iter__(self):
        return iter(self.__table.items())

    def __len__(self):
        return len(self.__table.keys())

    def action(self, current_state, input_character):

        def wrapper(transition_action):
            condition = Condition(current_state, input_character)
            if condition in self.__table:
                raise DuplicateCondition(*condition)

            self[condition] = transition_action

            @wraps(transition_action)
            def inner(*args, **kwargs):
                return transition_action(*args, **kwargs)

            return inner
        return wrapper

    def keys(self):
        return self.__table.keys()
