from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Course, Lesson, Learner, Enrollment, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson", "question_type", "grade")
    list_filter = ("question_type", "lesson__course")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "estimated_minutes")
    list_filter = ("course",)
    search_fields = ("title", "course__name")
    inlines = [QuestionInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "total_duration")
    search_fields = ("name",)
    inlines = [LessonInline]


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation")
    search_fields = ("user__username", "user__email")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("learner", "course", "date_enrolled")
    list_filter = ("course",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("learner", "lesson", "score", "total_questions", "submitted_at")
    list_filter = ("lesson__course", "submitted_at")
    readonly_fields = ("submitted_at",)

# Keep the built-in Authentication and Authorization section visible in admin.
# User and Group are supplied by django.contrib.auth and are intentionally not
# re-registered here.
