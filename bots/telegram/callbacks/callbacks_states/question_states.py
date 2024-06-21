from enum import Enum


class GenericState(str, Enum):
    yes = 'yes'
    no = 'no'


class CuratorState(str, Enum):
    yes = 'yes'
    no = 'no'


class GPTState(str, Enum):
    yes = 'yes'
    no = 'no'
    same = 'same'
    other = 'other'


class DemoWeekState(str, Enum):
    yes = 'yes'
    no = 'no'
    unsubscribe = 'unsubscribe'


class QuestionState(str, Enum):
    curator = 'curator'
    demo_week = 'demo_week'
    faq = 'faq'
    gpt = 'gpt'


class FAQState(str, Enum):
    end = 'main'
    back_to_universities = 'universities'
    back_to_programs = 'programs'
    back_to_questions = 'questions'
    back_to_sub_questions = 'sub_questions'


class ButtonState(int, Enum):
    university = 0
    program = 1
    question = 2
    sub_question = 3
    answer = 4
