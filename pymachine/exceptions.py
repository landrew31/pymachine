class DuplicateCondition(ValueError):
    def __init__(self, current_state, input_character, *args):
        message = (
            'Trying to add existing condition to transition table: from State'
            '(%s) with InputCharacter(%s)' % (current_state, input_character)
        )
        super(Exception, self).__init__(message, *args)


class StateMachineAlreadyFinished(Exception):
    def __init__(self, add_error_info=None, *args):
        message = 'State machine has already been in one of finish states.'
        if add_error_info:
            message = '. '.join([message, add_error_info])
        super(Exception, self).__init__(message, *args)


class StateMachineTransitionWithoutNextState(Exception):
    def __init__(self, state, input_character, add_error_info=None, *args):
        message = (
            'State machine has transition function without defining been next '
            'state. Transition from State(%s) for InputCharacter(%s).'
            % (state, input_character)
        )
        if add_error_info:
            message = '. '.join([message, add_error_info])
        super(Exception, self).__init__(message, *args)


class UnknownInput(Exception):
    def __init__(self, machine_input, add_error_info=None, *args):
        message = (
            'Unknown input: State(%s), InputCharacter(%s) for '
            'transition table.' % machine_input
        )
        if add_error_info:
            message = '. '.join([message, add_error_info])
        super(Exception, self).__init__(message, *args)


class UnknownState(ValueError):
    def __init__(self, state, add_error_info=None, *args):
        message = 'Unknown state %s for state machine.' % state
        if add_error_info:
            message = '. '.join([message, add_error_info])
        super(Exception, self).__init__(message, *args)
