from fastapi import FastAPI, UploadFile, HTTPException
from uuid import uuid4

from app.models import FileUploadResponse, FileResultResponse
from app.services.storage.storage_manager import StorageManager
from app.services.storage.mock_s3 import MockS3
from app.services.storage.mock_db import MockDB
from app.services.queue_manager import init_queue, enqueue_file, start_workers


app = FastAPI(title="CSV Processor")

# Create Storage Manager instance with Mocked S3 as file storage,
# and Mocked DB as the metadata storage
storage = StorageManager(file_storage=MockS3(), metadata_store=MockDB())

init_queue(storage)


@app.on_event("startup")
async def startup_event():
    start_workers(3)


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

    # Instead of doing the calculation here - send it to queue - for scale support
    await enqueue_file(file_id)

    return FileUploadResponse(file_id=file_id)


@app.get("/results/{file_id}", response_model=FileResultResponse)
async def get_results(file_id: str):
    rec = await storage.get_file_record(file_id)
    if not rec:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResultResponse.parse_obj(rec)
