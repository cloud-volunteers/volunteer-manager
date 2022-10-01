from argparse import ArgumentParser
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from common.config import Config
from common.logging import getCustomLogger
from app.db import database, User

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
    user, _ = await User.objects.get_or_create(email="test@test.com")
    logger.debug(f'Dummy user:\n{user.toPrintableJSON()}')
 
@app.on_event("shutdown")
async def shutdown():
    logger.info("Stopping db!")
    if database.is_connected:
        await database.disconnect()

@app.get("/items/{id}/{name}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id, "name": name})

@app.get("/volunteer", response_class=HTMLResponse)
async def read_item(request: Request):
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