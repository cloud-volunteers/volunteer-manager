from os import getenv
from uvicorn import run
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine, sessionlocal
from sqlalchemy.orm import Session
import models

models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title='Volunteer Manager', docs_url=None, redoc_url=None)
app = FastAPI(title='Volunteer Manager')

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# @app.get('/')
# async def root():
#     return {"info": "I'm software for managing volunteers!"}

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

# @app.get("/items/{id}/{name}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str, name: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id, "name": name})

@app.post("/add")
async def add(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    todo = models.Todo(task=task)
    db.add(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/edit/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo})

@app.post("/edit/{todo_id}")
async def add(request: Request, todo_id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

if __name__ == '__main__':
    run("server:app", host='0.0.0.0', port=int(getenv('PORT')))