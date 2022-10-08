from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import NamedTuple, Optional

from app.logging import getCustomLogger
from app.db import Student

logger = getCustomLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

class Student_dummy(NamedTuple):
    email: str
    phone: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[int] = None
    county: Optional[str] = None
    city_sector: Optional[str] = None
    online: Optional[bool] = False
    offline: Optional[bool] = False
    community: Optional[str] = None
    active: Optional[bool] = True

async def add_student_to_db(data):
    student, created = await Student.objects.get_or_create(email=data.get('email'))
    old_student = student.copy(deep=True)
    if data.get('county') is not None:
        student.county = data.get('county')
    student.online = data.get('online')
    student.offline = data.get('offline')
    if data.get('age') is not None:
        student.age = data.get('age')
    if student != old_student:
        await student.update()
        if created:
            logger.debug(f'Student added:\n{str(student)}')
        else:
            logger.debug(f'Student updated:\n{str(student)}')
        return student
    else:
        return None

@router.get("/student/{student_id}")
async def get_student(student_id: int, request: Request):
    try:
        student = await Student.objects.get(id=student_id)
    except Exception as e:
        return JSONResponse(content={'error': 'Student not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return student

@router.get("/students")
async def get_students(request: Request):
    all_students = await Student.objects.all()
    return all_students

@router.post("/student")
async def post_student(dummy_student: Student_dummy = Depends()):
    student = await add_student_to_db(dummy_student._asdict())
    if student is not None:
        return student
    else:
        return JSONResponse(content={'error': 'Student could not be added!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)