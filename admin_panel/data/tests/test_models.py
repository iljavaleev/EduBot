from django.test import TestCase

from ..models import (
    Program,
    ProgramName,
    Question,
    QuestionContent,
    SubQuestion,
    SubQuestionContent,
    University,
)


class UniversityTest(TestCase):

    def test_str_repr(self):
        university = University.objects.create(name='Test')
        self.assertEqual(str(university), university.name)


class ProgramTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.program: Program = Program.objects.create(
            program_name=ProgramName.objects.create(name='Test'),
            university=University.objects.create(name='Test')
        )

    def test_str_repr(self):
        program = ProgramTest.program
        self.assertEqual(
            str(program),
            f"{program.program_name.name} {program.university.name}"
        )


class QuestionTest(TestCase):

    def test_str_repr(self):
        question = Question.objects.create(
            question=QuestionContent.objects.create(title='Test'),
            program=Program.objects.create(
                program_name=ProgramName.objects.create(name='Test1'),
                university=University.objects.create(name='Test1')
            )
        )
        self.assertEqual(str(question), question.question.title)


class SubQuestionTest(TestCase):

    def test_str_repr(self):
        sub_question = SubQuestion.objects.create(
            content=SubQuestionContent.objects.create(
                text='TestQ',
                answer='TestA'
            ),
            question=QuestionContent.objects.create(
                title='TestTitle'
            )
        )
        self.assertEqual(str(sub_question), sub_question.content.text)
