from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import NamedTuple, Optional

from app.logging import getCustomLogger
from app.db import Volunteer, Student, Lesson

logger = getCustomLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
WEEKEND = ['Saturday', 'Sunday']
HOURS = ['09:00-12:00', '14:00-16:00', '16:00-19:00']
SUBJECTS = ['reading_and_writing_homework',
       'romanian_homework', 'math_homework', 'chemistry_homework',
       'history_homework', 'physics_homework', 'biology_homework',
       'french_homework', 'geography_homework', 'english_homework',
       'romanian_8th_grade_exam', 'romanian_12th_grade_exam',
       'math_8th_grade_exam', 'math_12th_grade_exam',
       'physics_12th_grade_exam', 'chemistry_12th_grade_exam',
       'geography_12th_grade_exam', 'biology_12th_grade_exam',
       'sociology_12th_grade_exam', 'history_12th_grade_exam',
       'vocational_counseling_workshops', 'online_safety_workshops',
       'games_and_personal_development_activities_workshops',
       'mentorship_for_teenagers_workshops', 'health_education_workshops',
       'financial_education_workshops', 'civic_education_workshops',
       'how_to_use_the_computer_workshops']

class Lesson_dummy(NamedTuple):
    volunteer: Volunteer
    student: Optional[Student] = None
    subject: Optional[str] = None
    week_day: Optional[str] = None
    time: Optional[str] = None
    remote: Optional[bool] = True
    active: Optional[bool] = True

async def add_lessons_to_db(data, volunteer):
    dummy_lessons = []
    for day in WEEKDAYS:
        if data.get(day):
            for hour in HOURS[1:]:
                if data.get(hour):
                    for subject in SUBJECTS:
                        if data.get(subject):
                            dummy_lesson = Lesson_dummy(
                                volunteer = volunteer,
                                subject = subject,
                                week_day = day,
                                time = hour,
                                remote = data.get('online'),
                            )
                            dummy_lessons.append(dummy_lesson)
    for day in WEEKEND:
        if data.get(day):
            for hour in HOURS:
                if data.get(hour):
                    for subject in SUBJECTS:
                        if data.get(subject):
                            dummy_lesson = Lesson_dummy(
                                volunteer = volunteer,
                                subject = subject,
                                week_day = day,
                                time = hour,
                                remote = data.get('online'),
                            )
                            dummy_lessons.append(dummy_lesson)
    for dummy_lesson in dummy_lessons:
        lesson, created = await Lesson.objects.get_or_create(dummy_lesson._asdict())
        if created:
            logger.debug(f'Lesson added:\n{lesson.toPrintableJSON()}')

@router.get("/lessons", response_class=HTMLResponse, tags=["lessons"])
async def get_lessons(request: Request):
    all_lessons = await Lesson.objects.all()
    return JSONResponse(content={'lessons': all_lessons}, status_code=status.HTTP_200_OK)
    # return templates.TemplateResponse("lessons.jinja.html", {"request": request, "lessons": all_lessons})

@router.get("/lesson/{lesson_id}", response_class=HTMLResponse, tags=["lessons"])
async def get_volunteer(lesson_id: int, request: Request):
    try:
        lesson = await Volunteer.objects.get(id=lesson_id)
    except Exception as e:
        return JSONResponse(content={'error': 'Lesson not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return lesson