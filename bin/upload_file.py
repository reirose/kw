import datetime
import re
from typing import NamedTuple, Optional
from time import time

from fastapi import File

from bin.db_init import kw_db
from bin.file_processing import extract_text_and_language
from bin.text_processing import process_text


class UploadResponse(NamedTuple):
    response_code: str
    error: Optional[Exception]
    data: Optional[dict]


async def upload_file(file: File):
    filename_wo_ext, ext = re.match("(.+)\.(.+)", file.filename).group(1), \
        re.match("(.+)\.(.+)", file.filename).group(2)
    file.filename = f"{filename_wo_ext}_{str(int(time()))}.{ext}"
    try:
        f = open(f"./files/{file.filename}", "x+b")
        f.write(await file.read())
    except Exception as e:
        # print(e)
        return UploadResponse("error", e, {"filename": file.filename})
    # contents = await file.read()
    contents, lang = extract_text_and_language(file_path=f"./files/{file.filename}")
    # print(contents, lang)
    kw = process_text(contents, lang)
    kw = [x.lower() for x in kw]
    kw_db.insert_one({"keyword": kw,
                      "docname": file.filename,
                      "lang": lang,
                      "url": f"download/{file.filename}",
                      "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M")})

    return UploadResponse("success", None, {"filename": file.filename, "keywords": " ".join(kw)})
