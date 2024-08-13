import os
from fastapi import HTTPException, UploadFile
from pathlib import Path
import aiofiles
import uuid

BASEDIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.abspath(os.path.join(BASEDIR, '..', 'static', 'images'))


async def handle_file_upload(file: UploadFile) -> str:
    _, ext = os.path.splitext(file.filename)
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join(IMAGE_DIR, file_name), mode='wb') as f:
        await f.write(content)

    return file_name

def handle_file_deletion(file_path: str):
    full_path = os.path.join(IMAGE_DIR, file_path)
    os.remove(full_path)
    