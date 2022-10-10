from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import NamedTuple, Optional
from json import dumps

from app.logging import getCustomLogger
from app.db import Volunteer, Student, Lesson, Possible_Lesson, Needed_Lesson
from algorithm.get_matching import matching_function
from itertools import product

logger = getCustomLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
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
    volunteer: Optional[Volunteer] = None
    student: Optional[Student] = None
    subject: Optional[str] = None
    week_day: Optional[str] = None
    time: Optional[str] = None
    remote: Optional[bool] = True

async def add_possible_lessons_to_db(data, volunteer):
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
    logger.debug(f'There are {len(dummy_lessons)} lessons!')
    await Possible_Lesson.objects.delete(volunteer=volunteer)
    for dummy_lesson in dummy_lessons:
        lesson = await Possible_Lesson.objects.create(
            volunteer = dummy_lesson.volunteer,
            subject = dummy_lesson.subject,
            week_day = dummy_lesson.week_day,
            time = dummy_lesson.time,
            remote = dummy_lesson.remote
            )
        logger.debug(f'Lesson added:\n{lesson.to_dict()}')

async def add_needed_lessons_to_db(data, student):
    dummy_lessons = []
    for day in WEEKDAYS:
        if data.get(day):
            for hour in HOURS[1:]:
                if data.get(hour):
                    for subject in SUBJECTS:
                        if data.get(subject):
                            dummy_lesson = Lesson_dummy(
                                student = student,
                                subject = subject,
                                week_day = day,
                                time = hour,
                                remote = True,
                            )
                            dummy_lessons.append(dummy_lesson)
    for day in WEEKEND:
        if data.get(day):
            for hour in HOURS:
                if data.get(hour):
                    for subject in SUBJECTS:
                        if data.get(subject):
                            dummy_lesson = Lesson_dummy(
                                student = student,
                                subject = subject,
                                week_day = day,
                                time = hour,
                                remote = True,
                            )
                            dummy_lessons.append(dummy_lesson)
    
    logger.debug(f'There are {len(dummy_lessons)} lessons!')
    await Needed_Lesson.objects.delete(student=student)
    for dummy_lesson in dummy_lessons:
        lesson = await Needed_Lesson.objects.create(
            student = dummy_lesson.student,
            subject = dummy_lesson.subject,
            week_day = dummy_lesson.week_day,
            time = dummy_lesson.time,
            remote = dummy_lesson.remote
            )
        logger.debug(f'Lesson added:\n{lesson.to_dict()}')


@router.get("/lessons", response_class=HTMLResponse, tags=["lessons"])
async def get_lessons(request: Request):
    # all_lessons = await Lesson.objects.filter(student__isnull=False).all()
    all_lessons = await Lesson.objects.all()
    lessons = [lesson.to_dict() for lesson in all_lessons]
    return templates.TemplateResponse("lessons.jinja.html", {"request": request, "lessons": lessons})

@router.get("/possible_lessons", response_class=HTMLResponse, tags=["lessons"])
async def get_possible_lessons(request: Request):
    all_lessons = await Possible_Lesson.objects.all()
    lessons = [lesson.to_dict() for lesson in all_lessons]
    return templates.TemplateResponse("lessons.jinja.html", {"request": request, "lessons": lessons})

@router.get("/needed_lessons", response_class=HTMLResponse, tags=["lessons"])
async def get_needed_lessons(request: Request):
    all_lessons = await Needed_Lesson.objects.all()
    lessons = [lesson.to_dict() for lesson in all_lessons]
    return templates.TemplateResponse("lessons.jinja.html", {"request": request, "lessons": lessons})

@router.get("/lessons/{subject}", response_class=HTMLResponse, tags=["lessons"])
async def get_lessons(subject: str, request: Request):
    # all_lessons = await Lesson.objects.filter(student__isnull=False).all()
    all_lessons = await Lesson.objects.filter(subject=subject).all()
    lessons = [lesson.to_dict() for lesson in all_lessons]
    return templates.TemplateResponse("lessons.jinja.html", {"request": request, "lessons": lessons})

@router.get("/lesson/{lesson_id}", response_class=HTMLResponse, tags=["lessons"])
async def get_lesson(lesson_id: int, request: Request):
    try:
        lesson = await Lesson.objects.get(id=lesson_id)
        print(lesson)
    except Exception as e:
        return JSONResponse(content={'error': 'Lesson not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content={'lesson': lesson.to_dict()}, status_code=status.HTTP_200_OK)

@router.get("/predict", response_class=HTMLResponse, tags=["lessons"])
async def predict_lessons(request: Request):
    await Lesson.objects.delete(active=True)
    await Possible_Lesson.objects.update(each=True, active=True)
    await Needed_Lesson.objects.update(each=True, active=True)

    for day in DAYS:
        for hour in HOURS:
            dummy_lessons = []
            needed_lessons = await Needed_Lesson.objects.filter(active=True).all()
            needed_lessons = [lesson.to_dict() for lesson in needed_lessons]
            possible_lessons = await Possible_Lesson.objects.filter(active=True).all()
            possible_lessons = [lesson.to_dict() for lesson in possible_lessons]

            all_needed_lessons = []
            for item in needed_lessons:
                if (item.get('week_day') == day) & (item.get('time') == hour):
                    all_needed_lessons.append(item)
            all_possible_lessons = []
            for item in possible_lessons:
                if (item.get('week_day') == day) & (item.get('time') == hour):
                    all_possible_lessons.append(item)

            all_possible_matches = []
            for subject in SUBJECTS:
                filtered_needed_lessons = [lesson.get('id') for lesson in all_needed_lessons if (lesson.get('subject') == subject)]
                filtered_possible_lessons = [lesson.get('id') for lesson in all_possible_lessons if (lesson.get('subject') == subject)]
                if len(filtered_needed_lessons) > 0 & len(filtered_possible_lessons):
                    all_possible_matches += list(product(filtered_needed_lessons, filtered_possible_lessons))

            final_matches = matching_function(all_possible_matches)
            final_matches_corrected = []
            for (x_f,y_f) in final_matches:
                for (x,y) in all_possible_matches:
                    if (x_f == x and y_f == y) or (x_f == y and y_f == x):
                        final_matches_corrected.append((x,y))

            for (x,y) in final_matches_corrected:
                possible_lesson = await Possible_Lesson.objects.get(id=y)
                needed_lesson = await Needed_Lesson.objects.get(id=x)
                dummy_lesson = Lesson_dummy(
                                volunteer = possible_lesson.volunteer,
                                student = needed_lesson.student,
                                subject = needed_lesson.subject,
                                week_day = day,
                                time = hour,
                                remote = True
                            )
                dummy_lessons.append(dummy_lesson)

            for dummy_lesson in dummy_lessons:
                student_colision_lessons = await Lesson.objects.filter(
                    student = dummy_lesson.student,
                    week_day = dummy_lesson.week_day,
                    time = dummy_lesson.time
                    ).all()
                volunteer_colision_lessons = await Lesson.objects.filter(
                    volunteer = dummy_lesson.volunteer,
                    week_day = dummy_lesson.week_day,
                    time = dummy_lesson.time
                    ).all()
                if len(student_colision_lessons) < 1 and len(volunteer_colision_lessons) < 1:
                    lesson = await Lesson.objects.create(
                        volunteer = dummy_lesson.volunteer,
                        student = dummy_lesson.student,
                        subject = dummy_lesson.subject,
                        week_day = dummy_lesson.week_day,
                        time = dummy_lesson.time,
                        remote = dummy_lesson.remote
                        )
                    logger.debug(f'Lesson added:\n{lesson.to_dict()}')
                    await Needed_Lesson.objects.filter(
                        student = dummy_lesson.student,
                        subject = dummy_lesson.subject
                        ).update(each=True, active=False)
                    await Needed_Lesson.objects.filter(
                        student = dummy_lesson.student,
                        week_day = dummy_lesson.week_day,
                        time = dummy_lesson.time
                        ).update(each=True, active=False)
                    # Allows volunteers take more than 1 lesson
                    # await Possible_Lesson.objects.filter(
                    #     volunteer = dummy_lesson.volunteer,
                    #     week_day = dummy_lesson.week_day,
                    #     time = dummy_lesson.time
                    #     ).update(each=True, active=False)

                    # Artifially give one volunteer only 1 lesson
                    await Possible_Lesson.objects.filter(
                        volunteer = dummy_lesson.volunteer
                        ).update(each=True, active=False)

    return RedirectResponse("/lessons", status_code=status.HTTP_302_FOUND)