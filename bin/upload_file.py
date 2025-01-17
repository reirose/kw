import datetime
import os
import re
from typing import NamedTuple, Optional
from time import time

from fastapi import File, UploadFile

from bin.db_init import kw_db
from bin.file_processing import extract_text_and_language
from bin.text_processing import process_text

if not os.path.exists("./files"):
    os.makedirs("./files")

class UploadResponse(NamedTuple):
    response_code: str
    error: Optional[Exception]
    data: Optional[dict]


async def upload_file(file: UploadFile):
    filename_wo_ext, ext = re.match("(.+)\.(.+)", file.filename).group(1), \
        re.match("(.+)\.(.+)", file.filename).group(2)
    file.filename = f"{filename_wo_ext}_{str(int(time()))}.{ext}"
    try:
        file.file.seek(0)
        contents = await file.read()
        if not contents:
            print("File contents are empty before saving!")
        with open(f"./files/{file.filename}", "wb") as f:
            f.write(contents)
    except Exception as e:
        return UploadResponse("error", e, {"filename": file.filename})
    contents, lang = extract_text_and_language(file_path=f"./files/{file.filename}")
    raw_kw = process_text(contents, lang)
    print(4, raw_kw)
    kw = []
    for x in raw_kw:
        try:
            kw.append(x.lower())
        except AttributeError:
            continue
    # kw = [x.lower() for x in kw]
    kw_db.insert_one({"keyword": kw,
                      "docname": file.filename,
                      "lang": lang,
                      "url": f"download/{file.filename}",
                      "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M")})

    return UploadResponse("success", None, {"filename": file.filename, "keywords": " ".join(kw)})
