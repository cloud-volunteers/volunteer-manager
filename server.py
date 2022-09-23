from os import getenv
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# app = FastAPI(title='Volunteer Manager', docs_url=None, redoc_url=None)
app = FastAPI(title='Volunteer Manager')

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/')
async def root():
    return {"info": "I'm software for managing volunteers!"}

@app.get("/items/{id}/{name}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id, "name": name})

if __name__ == '__main__':
    run("server:app", host='0.0.0.0', port=int(getenv('PORT')))