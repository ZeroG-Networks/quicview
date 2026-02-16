from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qlog import LogFile

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

# TODO: Replace.
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/v1/logfiles")
async def get_logfiles():
    return {} # TODO

@app.post("/v1/logfiles")
async def create_logfile():
    return {} # TODO

@app.delete("v1/logfiles/{logfile_id}")
async def delete_logfile(logfile_id):
    return {} # TODO

@app.get("/v1/logfiles/{logfile_id}")
async def read_logfile(logfile_id):
    return {} # TODO
