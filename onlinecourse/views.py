from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Lesson, Question, Submission


def course_list(request):
    courses = Course.objects.prefetch_related("lessons").all()
    return render(request, "onlinecourse/course_list.html", {"course_list": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related("lessons"), pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


def lesson_details(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.prefetch_related("questions__choices").select_related("course"),
        pk=lesson_id,
    )
    return render(request, "onlinecourse/lesson_details.html", {"lesson": lesson})


@login_required
def submit(request, lesson_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Exam answers must be submitted with POST.")

    lesson = get_object_or_404(Lesson.objects.prefetch_related("questions__choices"), pk=lesson_id)
    questions = list(lesson.questions.all())
    score = 0
    answers = {}
    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        if selected_id:
            try:
                selected_id_int = int(selected_id)
            except (TypeError, ValueError):
                selected_id_int = None
            choice = question.choices.filter(pk=selected_id_int).first() if selected_id_int else None
            if choice:
                answers[str(question.id)] = choice.id
                if choice.is_correct:
                    score += question.grade

    total = sum(question.grade for question in questions)
    submission = Submission.objects.create(
        learner=request.user,
        lesson=lesson,
        score=score,
        total_questions=total,
        answers=answers,
    )
    return redirect("onlinecourse:show_exam_result", submission_id=submission.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("learner", "lesson", "lesson__course"),
        pk=submission_id,
    )
    if submission.learner_id != request.user.id and not request.user.is_staff:
        return HttpResponseBadRequest("You do not have permission to view this result.")

    questions = submission.lesson.questions.prefetch_related("choices").all()
    result_rows = []
    for question in questions:
        selected_id = submission.answers.get(str(question.id))
        selected_choice = question.choices.filter(pk=selected_id).first() if selected_id else None
        correct_choice = question.choices.filter(is_correct=True).first()
        result_rows.append({
            "question": question,
            "selected_choice": selected_choice,
            "correct_choice": correct_choice,
            "is_correct": bool(selected_choice and selected_choice.is_correct),
        })

    return render(
        request,
        "onlinecourse/exam_result.html",
        {"submission": submission, "result_rows": result_rows},
    )
