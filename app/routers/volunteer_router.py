from fastapi import APIRouter, Request, File, UploadFile, Depends, status, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import NamedTuple, Optional
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from pathlib import Path

from app.logging import getCustomLogger
from app.functions import process_voluneteer_excel
from app.db import Volunteer
from app.routers.lesson_router import add_possible_lessons_to_db

logger = getCustomLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

class Volunteer_dummy(NamedTuple):
    id: int
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


async def add_volunteer_to_db(data, excel=False):
    id = data.get('id')
    volunteer = None
    created = None
    
    if(id is not None):
        volunteer = await Volunteer.objects.get_or_none(id=id)
        created = False

    if(volunteer is None):
        if excel:
            volunteer, created = await Volunteer.objects.get_or_create(email=data.get('email'))
        else:
            try:
                volunteer, created = await Volunteer.objects.create(email=data.get('email'))
            except Exception as e:
                logger.error(f'{str(e)}')
                return None

    old_volunteer = volunteer.copy(deep=True)
    for field in ['email', 'phone', 'county', 'city_sector', 'online', 'offline', 'has_car', 'age', 'status', 'active']:
        volunteer[field] = data.get(field)

    if volunteer != old_volunteer:
        await volunteer.update()
        if created:
            logger.debug(f'Volunteer added:\n{str(volunteer)}')
        else:
            logger.debug(f'Volunteer updated:\n{str(volunteer)}')
        return volunteer
    else:
        return None

@router.get("/upload_volunteer_excel", tags=["volunteers"])
async def webpage_volunteer_excel(request: Request):
    return templates.TemplateResponse("upload_volunteer_excel.jinja.html", {"request": request})

@router.post("/upload_volunteer_excel", tags=["volunteers"])
async def upload_volunteers_excel_file(files: list[UploadFile]):
    for file in files:
        try:    
            suffix = Path(file.filename).suffix.lower()
            with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
                copyfileobj(file.file, tmp)
                new_data = process_voluneteer_excel(tmp)
        except Exception as e:
            logger.error(str(e))
            return JSONResponse(content={'error': 'Excel file can not be loaded!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        finally:
            file.file.close()
        for data in new_data:
            volunteer = await add_volunteer_to_db(data, excel=True)
            if volunteer is not None:
                await add_possible_lessons_to_db(data, volunteer)

    return RedirectResponse("/volunteers", status_code=status.HTTP_302_FOUND)

@router.get("/volunteer/{volunteer_id}", response_class=HTMLResponse, tags=["volunteers"])
async def get_volunteer(volunteer_id: int, request: Request):
    try:
        volunteer = await Volunteer.objects.get(id=volunteer_id)
    except Exception as e:
        return JSONResponse(content={'error': 'Volunteer not found!'}, status_code=status.HTTP_404_NOT_FOUND)

    return templates.TemplateResponse("volunteer.jinja.html", {"request": request, "volunteer": {"id": str(volunteer.id), "email": str(volunteer.email), "online": str(volunteer.online), "offline": str(volunteer.offline), "county": str(volunteer.county), "age": str(volunteer.age), "active": bool(volunteer.active), "has_car": bool(volunteer.has_car), "city_sector": str(volunteer.city_sector), "phone": str(volunteer.phone)}})

@router.get("/volunteers", response_class=HTMLResponse, tags=["volunteers"])
async def get_volunteers(request: Request):
    all_volunteers = await Volunteer.objects.all()
    #return all_volunteers
    return templates.TemplateResponse("volunteers.jinja.html", {"request": request, "volunteers": all_volunteers})

@router.get("/volunteer", tags=["volunteers"])
async def new_volunteer(request: Request):
    return templates.TemplateResponse("newvolunteer.jinja.html", {"request": request})

@router.post("/volunteer", tags=["volunteers"])
async def post_volunteer(id: int = Form(None), email: str = Form(), online: bool = Form(False), offline: bool = Form(False), county: str = Form(None), age: int = Form(None), phone: str = Form(None), city_sector: str = Form(None), has_car: bool = Form(False), active: bool = Form(False)):
#async def post_volunteer(dummy_volunteer: Volunteer_dummy = Depends()):
    dummy_volunteer = Volunteer_dummy(id=id, email=email, online=online, offline=offline, county=county, age=age,phone=phone,has_car=has_car, city_sector=city_sector, active=active)

    volunteer = await add_volunteer_to_db(dummy_volunteer._asdict())
    if volunteer is not None:
        #return volunteer
        return RedirectResponse("/volunteer/{:d}".format(volunteer.id), status_code=status.HTTP_302_FOUND)
    else:
        return JSONResponse(content={'error': 'Volunteer could not be added!'}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
