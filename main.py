import uvicorn
import os

from typing import Optional

from fastapi import Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from bin.data_processing import get_data
from bin.db_init import client
from bin.init import app, templates, files
from bin.text_processing import process_text
from bin.upload_file import upload_file, UploadResponse


@app.on_event("startup")
async def startup() -> None:
    print("App running")


@app.on_event("shutdown")
async def shutdown() -> None:
    client.close()
    print("App stopped")


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(files, filename)
    if os.path.isfile(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get('/search', response_class=templates.TemplateResponse)
@app.get('/', response_class=templates.TemplateResponse)
async def root(request: Request, q: Optional[str] = ""):
    data = {"status": "ok",
            "info": get_data(q.lower())}
    if not data["info"]:
        data["status"] = "error"

    return templates.TemplateResponse(
        name="index.html",
        context={"data": data,
                 "request": request}
    )


@app.get("/upload", response_class=templates.TemplateResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        name="upload.html",
        context={"request": request,
                 "data": {"response_code": "ok", "error": None, "data": None}}
    )


@app.post('/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    if not any([file.filename, file.size]):
        data = UploadResponse("error", None, {"filename": "файла: файл не выбран."})
        return templates.TemplateResponse(
            name="upload.html",
            context={"request": request,
                     "data": data}
        )
    data = await upload_file(file)
    if data.error:
        return templates.TemplateResponse(
            name="upload.html",
            context={"request": request,
                     "data": data}
        )
    return templates.TemplateResponse(
        name="upload.html",
        context={"request": request,
                 "data": data}
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app,
                host='0.0.0.0',
                port=27015)
