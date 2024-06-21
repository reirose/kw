import re
from typing import NamedTuple, Optional
from time import time

from fastapi import File

from bin.db_init import kw_db
from bin.text_processing import process_text


class UploadResponse(NamedTuple):
    response_code: str
    error: Optional[Exception]
    data: Optional[dict]


async def upload_file(file: File):
    filename_wo_ext, ext = re.match("(.+)\.(.+)", file.filename).group(1), \
        re.match("(.+)\.(.+)", file.filename).group(2)
    file.filename = f"{filename_wo_ext}_{str(int(time()))}.{ext}"
    contents = await file.read()
    kw = process_text(contents.decode("utf-8"))
    kw_db.insert_one({"keyword": kw, "docname": file.filename, "lang": "", "url": f"download/{file.filename}"})

    try:
        with open(f"files/{file.filename}", "w+b") as f:
            f.write(contents)
    except Exception as e:
        return UploadResponse("error", e, {"filename": file.filename})
    return UploadResponse("success", None, {"filename": file.filename, "keywords": " ".join(kw)})
