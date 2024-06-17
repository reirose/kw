import uvicorn

from fastapi import Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from bin.init import app, templates


@app.on_event("startup")
async def startup() -> None:
    print("App running")


@app.on_event("shutdown")
async def shutdown() -> None:
    print("App stopped")


@app.get('/')
async def root(request: Request, response_class=HTMLResponse):
    data = {"status": "ok",
            "info": [{"kw": "hello", "docname": "world", "lang": "ru", "url": "/"},
                     {"kw": "1", "docname": "2", "lang": "ru", "url": "/"}]}
    return templates.TemplateResponse(
        name="index.html",
        context={"data": data,
                 "request": request}
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app,
                host='0.0.0.0',
                port=27015)
