from unittest import TestCase

from pymachine import (
    StateMachine,
    TransitionTable,
    StateMachineAlreadyFinished,
)


STATES = (
    Q1,
    Q2,
    Q3,
    STOP,
) = range(4)
B = ''
ZERO = '0'
ONE = '1'


class TestStateMachine(StateMachine):
    """
    Classical Turing Machine automaton. Adds 1 to binary number.
    Formal representation^

    1Q1 -> 1Q1R
    0Q1 -> 0Q1R
    BQ1 -> BQ2L
    1Q2 -> 0Q1L
    0Q2 -> 1Q3L
    BQ2 -> 1STOP
    1Q3 -> 1Q3L
    0Q3 -> 0Q3L
    BQ3 -> BSTOP

    Q1, Q2, Q3, STOP - states
    0, 1, B - alphabet, B - empty symbol

    """

    TT = TransitionTable()

    def __init__(self, number):
        if not isinstance(number, str):
            raise TypeError('Expected string. Got %s' % type(number))

        self.number = list(number)
        self.index = 0
        super(TestStateMachine, self).__init__(Q1, STATES, (STOP,))

    @TT.action(Q1, ONE)
    def _1q1(self):
        self.index += 1
        self.next_state = Q1

    @TT.action(Q1, ZERO)
    def _0q1(self):
        self.index += 1
        self.next_state = Q1

    @TT.action(Q1, B)
    def _bq1(self):
        self.index -= 1
        self.next_state = Q2

    @TT.action(Q2, ONE)
    def _1q2(self):
        if self.index >= 0:
            self.number[self.index] = ZERO
        self.index -= 1
        self.next_state = Q2

    @TT.action(Q2, ZERO)
    def _0q2(self):
        if self.index >= 0:
            self.number[self.index] = ONE
        self.index -= 1
        self.next_state = Q3

    @TT.action(Q2, B)
    def _bq2(self):
        if self.index >= 0:
            self.number[self.index] = ONE
        else:
            self.number.insert(0, ONE)
        self.next_state = STOP

    @TT.action(Q3, ONE)
    def _1q3(self):
        self.index -= 1
        self.next_state = Q3

    @TT.action(Q3, ZERO)
    def _0q3(self):
        self.index -= 1
        self.next_state = Q3

    @TT.action(Q3, B)
    def _bq3(self):
        self.index += 1
        self.next_state = STOP

    def get_value(self):
        return ''.join(self.number)

    def get_next_input(self):
        if self.index < 0:
            return B
        if self.index >= len(self.number):
            return B
        return self.number[self.index]

    def run(self):
        input_ = self.number[self.index]
        try:
            while True:
                self.move(input_)
                input_ = self.get_next_input()
        except StateMachineAlreadyFinished:
            return self.get_value()


class TuringStateMachineTestCase(TestCase):
    def test_turing_machine_add_one_to_binary(self):
        turing_machine = TestStateMachine('10000')
        self.assertEqual('10001', turing_machine.run())

        turing_machine = TestStateMachine('111')
        self.assertEqual('1000', turing_machine.run())
