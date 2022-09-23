from os import getenv
from uvicorn import run
from fastapi import FastAPI

# app = FastAPI(title='Volunteer Manager', docs_url=None, redoc_url=None)
app = FastAPI(title='Volunteer Manager')

@app.get('/')
async def root():
    return {"info": "I'm software for managing volunteers!"}

if __name__ == '__main__':
    run("server:app", host='0.0.0.0', port=int(getenv('PORT')))