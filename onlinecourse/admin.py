from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("content", "course", "grade")
    list_filter = ["course"]
    search_fields = ["content"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
