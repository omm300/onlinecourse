# Django Online Course — Assessment Final Project

A runnable Django Online Course demo with courses, lessons, questions, choices, exam submission, score calculation, and exam-result display.

## Requirements
- Python 3.10+
- pip

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Run locally (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Create demo content
1. Log in to `/admin/`.
2. Add a Course with a title, description, and total duration.
3. Add one or more Lessons and link each lesson to the course.
4. Open a lesson and add Questions using the Questions inline.
5. Add Choices for each question using the Choices inline. Select the correct choice.
6. Visit the course page, open a lesson, and submit the mock exam.

## Submission file paths
- `onlinecourse/models.py`
- `onlinecourse/admin.py`
- `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
- `onlinecourse/views.py`
- `onlinecourse/urls.py`

These files implement the requested models, admin classes, course template, `submit`, and `show_exam_result` functions.

## Notes
This is a complete starter implementation for the assignment. Review it, run it, add your own demo course/questions, and capture genuine screenshots from your own running app. Do not upload a database containing your personal information or credentials.
