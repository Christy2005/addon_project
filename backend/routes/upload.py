from fastapi import APIRouter, UploadFile, File
import shutil
import os

from parser.pdf_parser import extract_text

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    report_text = extract_text(file_path)

    return {
        "filename": file.filename,
        "report_text": report_text
    }