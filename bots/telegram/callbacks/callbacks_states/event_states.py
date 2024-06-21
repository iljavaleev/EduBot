from enum import Enum


class GenericEventState(str, Enum):
    yes = 'yes'
    no = 'no'


class StartEventState(str, Enum):
    next = 'next'
    previous = 'previous'


class NotificationChoiceState(int, Enum):
    now = 2
    hour = 0
    moment = 1


class RepeatChoiceOrExitState(str, Enum):
    repeat = 'repeat'
    exit = 'exit'
