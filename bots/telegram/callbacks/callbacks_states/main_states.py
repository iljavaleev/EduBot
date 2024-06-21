from enum import Enum


class MainState(str, Enum):
    question = 'question'
    article = 'article'
    events = 'events'
