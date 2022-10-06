from uvicorn import run
from fastapi import FastAPI, Request, File, UploadFile, Depends, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from pathlib import Path
from typing import NamedTuple, Optional
from json import loads, dumps

from app.config import Config
from app.logging import getCustomLogger
from app.db import database, Volunteer, Student
from app.functions import process_excel

logger = getCustomLogger(__name__)

app = FastAPI(title=Config.APP_NAME, docs_url='/docs', redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")

class Volunteer_dummy(NamedTuple):
    email: str
    phone: Optional[str] = None
    county: Optional[str] = None
    city_sector: Optional[str] = None
    online: Optional[bool] = False
    offline: Optional[bool] = False
    has_car: Optional[bool] = False
    age: Optional[int] = None
    status: Optional[str] = None
    active: Optional[bool] = True

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

async def add_volunteer_to_db(data):
    volunteer, created = await Volunteer.objects.get_or_create(email=data.get('email'))
    old_volunteer = volunteer.copy(deep=True)
    if data.get('county') is not None:
        volunteer.county = data.get('county')
    volunteer.online = data.get('online')
    volunteer.offline = data.get('offline')
    if data.get('age') is not None:
        volunteer.age = data.get('age')
    if volunteer != old_volunteer:
        await volunteer.update()
        if created:
            logger.debug(f'Volunteer added:\n{str(volunteer)}')
        else:
            logger.debug(f'Volunteer updated:\n{str(volunteer)}')
        return volunteer
    else:
        return None

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

@app.get('/')
async def root():
    logger.warning('Root was called!')
    return {"info": "I'm software for managing volunteers!"}

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    volunteer, _ = await Volunteer.objects.get_or_create(email="test@test.com")
    logger.debug(f'Dummy volunteer:\n{volunteer.toPrintableJSON()}')
 
@app.on_event("shutdown")
async def shutdown():
    logger.info("Stopping db!")
    if database.is_connected:
        await database.disconnect()

@app.post("/upload_excel")
async def upload_excel_file(file: UploadFile = File(...)):
    try:    
        suffix = Path(file.filename).suffix.lower()
        with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
            copyfileobj(file.file, tmp)
            new_data = process_excel(tmp)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(content={'error': 'Excel file can not be loaded!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    finally:
        file.file.close()
    for data in new_data:
        await add_volunteer_to_db(data)
    return JSONResponse(content={'info': 'Excel file successfully loaded!'}, status_code=status.HTTP_200_OK)

@app.get("/volunteer/{volunteer_id}", response_class=HTMLResponse)
async def get_volunteer(volunteer_id: int, request: Request):
    try:
        volunteer = await Volunteer.objects.get(id=volunteer_id)
    except Exception as e:
        return JSONResponse(content={'error': 'Volunteer not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return templates.TemplateResponse("volunteer.jinja.html", {"request": request, "volunteer": {"id": str(volunteer.id), "email": str(volunteer.email), "online": str(volunteer.online), "offline": str(volunteer.offline), "county": str(volunteer.county), "age": str(volunteer.age)}})

@app.get("/volunteers")
async def get_volunteers(request: Request):
    all_volunteers = await Volunteer.objects.all()
    return all_volunteers

@app.post("/volunteer")
async def post_volunteer(dummy_volunteer: Volunteer_dummy = Depends()):
    volunteer = await add_volunteer_to_db(dummy_volunteer._asdict())
    if volunteer is not None:
        return volunteer
    else:
        return JSONResponse(content={'error': 'Volunteer could not be added!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.get("/student/{student_id}")
async def get_student(student_id: int, request: Request):
    try:
        student = await Student.objects.get(id=student_id)
    except Exception as e:
        return JSONResponse(content={'error': 'Student not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return student

@app.get("/students")
async def get_students(request: Request):
    all_students = await Student.objects.all()
    return all_students

@app.post("/student")
async def post_student(dummy_student: Student_dummy = Depends()):
    student = await add_student_to_db(dummy_student._asdict())
    if student is not None:
        return student
    else:
        return JSONResponse(content={'error': 'Student could not be added!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)