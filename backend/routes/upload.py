from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from parser.pdf_parser import extract_text

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):

    # Check if uploaded file is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        report_text = extract_text(file_path)

        return {
            "message": "Report uploaded successfully.",
            "filename": file.filename,
            "report_text": report_text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )