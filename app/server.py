from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import Config
from app.logging import getCustomLogger
from app.db import database, Volunteer
from app.routers import volunteer_router, student_router

logger = getCustomLogger(__name__)

app = FastAPI(title=Config.APP_NAME, docs_url='/docs', redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

@app.get('/')
async def root():
    logger.warning('Root was called!')
    return {"info": "I'm software for managing volunteers!"}

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    volunteer, created = await Volunteer.objects.get_or_create(email="test@test.com")
    if created:
        logger.debug(f'Dummy volunteer added:\n{volunteer.toPrintableJSON()}')
    else:
        logger.debug(f'Dummy volunteer updated:\n{volunteer.toPrintableJSON()}')
 
@app.on_event("shutdown")
async def shutdown():
    logger.info("Stopping db!")
    if database.is_connected:
        await database.disconnect()

app.include_router(volunteer_router.router)

app.include_router(student_router.router)