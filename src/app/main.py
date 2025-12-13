from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, UploadFile, HTTPException

from app.models import FileUploadResponse, FileResultResponse
from app.services.storage.storage_manager import StorageManager
from app.services.storage.mock_s3 import MockS3
from app.services.storage.mock_db import MockDB
from app.services.queue_manager import init_queue, enqueue_file, start_workers

# Create Storage Manager instance with Mocked S3 as file storage,
# and Mocked DB as the metadata storage
storage = StorageManager(file_storage=MockS3(), metadata_store=MockDB())

init_queue(storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_workers(3)
    yield


app = FastAPI(title="CSV Processor", lifespan=lifespan)

origins = ["http://localhost:5173"]  # allow Vite dev server

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return FileResultResponse.model_validate(rec)
