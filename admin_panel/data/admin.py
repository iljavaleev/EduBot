from django.contrib import admin
from django.db import models
from django.forms import Textarea
from import_export.admin import ImportExportModelAdmin

from .models import (
    Program,
    ProgramName,
    Question,
    QuestionContent,
    SubQuestion,
    SubQuestionContent,
    University,
)


class SubQuestionAdmin(admin.StackedInline):
    model = SubQuestion
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})},
    }


@admin.register(QuestionContent)
class QuestionContentAdmin(admin.ModelAdmin):
    save_as = True
    inlines = [SubQuestionAdmin]


@admin.register(SubQuestionContent)
class SubQuestionContentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    save_as = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'program']
    list_filter = ['program']

    def title(self, question: Question) -> str:
        return f"{question.question.title[:30]}..."

    def program(self, question: Question) -> str:
        return question.program.program_name.name


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(ProgramName)
class ProgramNameAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}
