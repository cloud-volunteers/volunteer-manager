from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.config import Config
from app.logging import getCustomLogger
from app.db import database, Volunteer
from app.routers import volunteer_router, student_router, lesson_router

logger = getCustomLogger(__name__)

app = FastAPI(title=Config.APP_NAME,
              description='App for managing volunteers!',
              version='0.0.9',
              terms_of_service='https://github.com/cloud-volunteers/volunteer-manager',
              contact={
                "name": "Cloud Volunteers",
              },
              license_info={
                "name": "MIT License",
                "url": "https://github.com/cloud-volunteers/volunteer-manager/blob/main/LICENSE",
              },
              docs_url='/docs',
              swagger_ui_parameters={"defaultModelsExpandDepth": -1},
              redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")

@app.get('/', include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.jinja.html", {"request": request})

@app.get('/health', include_in_schema=False)
async def health():
    logger.debug('Health was called!')
    try:
        await Volunteer.objects.get(email="test@test.com")
        return {"health": "OK!"}
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

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

app.include_router(lesson_router.router)