from fastapi import APIRouter, Request, Depends, status, Form, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import NamedTuple, Optional
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from pathlib import Path

from app.logging import getCustomLogger
from app.functions import process_student_excel
from app.db import Student
from app.routers.lesson_router import add_needed_lessons_to_db

logger = getCustomLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

class Student_dummy(NamedTuple):
    id: int
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

async def add_student_to_db(data, excel=False):
    id = data.get('id')
    student = None
    created = None
    
    if(id is not None):
        student = await Student.objects.get_or_none(id=id)
        created = False

    if(student is None):
        if excel:
            student, created = await Student.objects.get_or_create(email=data.get('email'))
        else:
            try:
                student, created = await Student.objects.create(email=data.get('email'))
            except Exception as e:
                logger.error(f'{str(e)}')
                return None

    old_student = student.copy(deep=True)
    for field in ['email', 'county', 'city_sector', 'online', 'offline', 'phone', 'age', 'active']:
        student[field] = data.get(field)

    if student != old_student:
        await student.update()
        if created:
            logger.debug(f'Student added:\n{str(student)}')
        else:
            logger.debug(f'Student updated:\n{str(student)}')
        return student
    else:
        return None

@router.get("/student/{student_id}", tags=["students"])
async def get_student(student_id: int, request: Request):
    try:
        student = await Student.objects.get(id=student_id)
    except Exception as e:
        return JSONResponse(content={'error': 'Student not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return templates.TemplateResponse("student.jinja.html", {"request": request, "student": {"id": str(student.id), "email": str(student.email), "online": str(student.online), "offline": str(student.offline), "county": str(student.county), "age": str(student.age), "active": bool(student.active), "city_sector": str(student.city_sector), "phone": str(student.phone)}})

@router.get("/students", tags=["students"])
async def get_students(request: Request):
    all_students = await Student.objects.all()
    return templates.TemplateResponse("students.jinja.html", {"request": request, "students": all_students})

@router.get("/student", tags=["students"])
async def new_student(request: Request):
    return templates.TemplateResponse("newstudent.jinja.html", {"request": request})

@router.post("/student", tags=["students"])
#async def post_student(dummy_student: Student_dummy = Depends()):
async def post_student(id: int = Form(None), email: str = Form(), online: bool = Form(False), offline: bool = Form(False), county: str = Form(None), age: int = Form(None), phone: str = Form(None), city_sector: str = Form(None), grade: int = Form(None), active: bool = Form(False)):
    dummy_student = Student_dummy(id=id, email=email, online=online, offline=offline, county=county, age=age,phone=phone,grade=grade, city_sector=city_sector, active=active)
    
    student = await add_student_to_db(dummy_student._asdict())
    if student is not None:
        #return student
        return RedirectResponse("/student/{:d}".format(student.id), status_code=status.HTTP_303_SEE_OTHER)
    else:
        return JSONResponse(content={'error': 'Student could not be added!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@router.get("/upload_student_excel", tags=["students"])
async def webpage_student_excel(request: Request):
    return templates.TemplateResponse("upload_student_excel.jinja.html", {"request": request})

@router.post("/upload_student_excel", tags=["students"])
async def upload_students_excel_file(files: list[UploadFile]):
    for file in files:
        try:    
            suffix = Path(file.filename).suffix.lower()
            with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
                copyfileobj(file.file, tmp)
                new_data = process_student_excel(tmp)
        except Exception as e:
            logger.error(str(e))
            return JSONResponse(content={'error': 'Excel file can not be loaded!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        finally:
            file.file.close()
        for data in new_data:
            student = await add_student_to_db(data, excel=True)
            if student is not None:
                await add_needed_lessons_to_db(data, student)

    return RedirectResponse("/students", status_code=status.HTTP_302_FOUND)