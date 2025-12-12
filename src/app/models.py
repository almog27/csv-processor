from pydantic import BaseModel
from typing import Dict, List, Optional, Any


class FileUploadResponse(BaseModel):
    file_id: str

class ErrorEntry(BaseModel):
    row: int
    error: str

class Aggregates(BaseModel):
    row_count: int
    min_value: float
    max_value: float
    mean_value: float
    per_sensor_count: Dict[str, int]


class FileResultResponse(BaseModel):
    file_id: str
    status: str
    aggregates: Optional[Aggregates] = None
    errors: List[ErrorEntry] = []
    duration_ms: int
    created_at: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
