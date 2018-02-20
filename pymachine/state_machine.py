from pymachine.condition import Condition
from pymachine.exceptions import (
    UnknownState,
    StateMachineAlreadyFinished,
    StateMachineTransitionWithoutNextState,
)
from pymachine.transition_table import TransitionTable


class StateMachine(object):

    TT = TransitionTable()

    def __init__(self, current_state, states, finish_states, **kwargs):
        self.states = states
        self.additional_error_message = kwargs.get('additional_error_message')

        self.alphabet = self.__get_alphabet(self.TT)

        if current_state not in self.states:
            raise UnknownState(current_state, self.additional_error_message)

        self.state = current_state
        self.next_state = None
        self.finish_states = finish_states

    @staticmethod
    def __get_alphabet(transition_table):
        return set(cond.input_character for cond in transition_table.keys())

    def move(self, input_character, **kwargs):
        if self.state in self.finish_states:
            raise StateMachineAlreadyFinished(self.additional_error_message)
        _input = Condition(self.state, input_character)
        executor = self.TT[_input]
        result = executor(self, **kwargs)

        if self.next_state is None:
            raise StateMachineTransitionWithoutNextState(
                self.state, input_character, self.additional_error_message)

        self.state = self.next_state
        self.next_state = None
        return result
