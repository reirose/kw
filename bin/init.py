import os

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

directory = "./files/"
if not os.path.exists(directory):
    os.makedirs(directory)

app = FastAPI(title="diplom",
              version="indev")
templates = Jinja2Templates(directory="templates")
files = "files"
