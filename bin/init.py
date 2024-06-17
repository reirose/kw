from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI(title="diplom",
              version="indev")
templates = Jinja2Templates(directory="lib/template")
