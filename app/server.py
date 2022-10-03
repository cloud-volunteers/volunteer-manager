from argparse import ArgumentParser
from uvicorn import run
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from pathlib import Path 

from app.config import Config
from app.logging import getCustomLogger
from app.db import database, Volunteer
from app.functions import process_excel

logger = getCustomLogger(__name__)

app = FastAPI(title=Config.APP_NAME, docs_url='/docs', redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")

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
    finally:
        file.file.close()
    for data in new_data:
        volunteer, created = await Volunteer.objects.get_or_create(email=data.get('email'))
        old_volunteer = volunteer.copy(deep=True)
        volunteer.county = data.get('county')
        volunteer.online = data.get('online')
        volunteer.offline = data.get('offline')
        volunteer.age = data.get('age')
        if volunteer != old_volunteer:
            await volunteer.update()
            if created:
                logger.debug(f'Volunteer added:\n{str(volunteer)}')
            else:
                logger.debug(f'Volunteer updated:\n{str(volunteer)}')

# @app.get("/volunteers/{volunteer_id}", response_class=HTMLResponse)
@app.get("/volunteers/{volunteer_id}")
async def get_volunteer(volunteer_id: int, request: Request):
    volunteer = await Volunteer.objects.get(id=volunteer_id)
    # return templates.TemplateResponse("volunteer.jinja.html", {"request": request, "volunteer": {"id": volunteer.id, "email": volunteer.email, "online": volunteer.online, "offline": volunteer.offline, "county": volunteer.county, "age": volunteer.age}})
    return volunteer