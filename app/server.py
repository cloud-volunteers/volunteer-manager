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
        new_volunteer = volunteer.copy(deep=True)
        new_volunteer.county = data.get('county')
        new_volunteer.online = data.get('online')
        new_volunteer.offline = data.get('offline')
        new_volunteer.age = data.get('age')
        changed = (new_volunteer != volunteer)
        await Volunteer.objects.bulk_update([new_volunteer])
        if created:
            logger.debug(f'Volunteer added:\n{str(new_volunteer)}')
        elif changed:
            logger.debug(f'Volunteer updated:\n{str(new_volunteer)}')

@app.get("/volunteer", response_class=HTMLResponse)
async def get_volunteer(request: Request):
    return templates.TemplateResponse("volunteer.jinja.html", {"request": request, "user": {"name": 'Mirek', 'email': 'mirek@email.pl', "phone": '123 456 789', "hasCar": 'Yes'}})

if __name__ == '__main__':
        
    parser = ArgumentParser(description='Websocket_api for connection to ML models')
    parser.add_argument('--port', dest='port', type = int,
                    default=8000,
                    help='port for connection')
    parser.add_argument('--log-level', dest='log_level', type=str,
                    default="info",
                    help='log level')
    args = parser.parse_args()
    
    run("server:app",
         host='0.0.0.0',
         port=args.port,
         log_level=args.log_level)