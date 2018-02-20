from collections import namedtuple

Condition = namedtuple(
    'Condition',
    ['current_state', 'input_character'],
)
