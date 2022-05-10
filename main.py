from cgitb import handler
from inspect import Parameter
from typing import Any,Dict
from fastapi import Body,FastAPI,Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn




app=FastAPI()
# add static files and templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")






@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})



@app.post('/background')
async def home(query:Request=str):
    
    
    return ''



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)