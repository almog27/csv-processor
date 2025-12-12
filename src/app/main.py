from fastapi import FastAPI, UploadFile, HTTPException
from uuid import uuid4
import asyncio

from src.app.models import FileUploadResponse, FileResultResponse
from src.app.services.storage.storage_manager import StorageManager
from src.app.services.storage.mock_s3 import MockS3
from src.app.services.storage.mock_db import MockDB

app = FastAPI(title="CSV Processor")

# Create Storage Manager instance with Mocked S3 as file storage,
# and Mocked DB as the metadata storage
storage = StorageManager(file_storage=MockS3(), metadata_store=MockDB())


@app.post("/upload", response_model=FileUploadResponse)
async def upload(file: UploadFile):
    # Read the file, and decode
    content_bytes = await file.read()
    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content = content_bytes.decode("latin-1")

    # Generate file id
    file_id = str(uuid4())

    await storage.upload_file(file_id, content)

    return FileUploadResponse(file_id=file_id)


@app.get("/results/{file_id}", response_model=FileResultResponse)
async def get_results(file_id: str):
    rec = await storage.get_file_record(file_id)
    if not rec:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResultResponse.parse_obj(rec)
