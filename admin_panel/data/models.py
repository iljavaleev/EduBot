from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name


class ProgramName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    program_name = models.ForeignKey(
        ProgramName,
        on_delete=models.CASCADE,
        verbose_name='Educational Program'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.program_name.name} {self.university.name}"


class QuestionContent(models.Model):
    title = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        verbose_name='Educational Program'
    )
    question = models.ForeignKey(
        QuestionContent,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question.title


class SubQuestionContent(models.Model):
    text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f'{self.text[:50]}...'


class SubQuestion(models.Model):
    question = models.ForeignKey(
        QuestionContent,
        on_delete=models.CASCADE,
        related_name='q'
    )
    content = models.ForeignKey(
        SubQuestionContent,
        on_delete=models.CASCADE,
        verbose_name='Sub Question',
        related_name='sub_questions'
    )

    class Meta:
        verbose_name = 'Sub Question'
        verbose_name_plural = 'Sub Questions'

    def __str__(self):
        return f'{self.content.text}'
