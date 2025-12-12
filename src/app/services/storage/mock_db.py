from typing import Dict, Optional, Any
import asyncio
import time

from src.app.services.storage.storage_interface import MetadataStore


class MockDB(MetadataStore):
    def __init__(self) -> None:
        self._records: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def insert_file_record(self, file_id: str, record: Dict[str, Any]) -> None:
        async with self._lock:
            rec = dict(record)
            rec.setdefault("created_at", time.time())
            rec["file_id"] = file_id
            self._records[file_id] = rec

    async def get_file_record(self, file_id: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            rec = self._records.get(file_id)
            return dict(rec) if rec is not None else None

    async def update_file_record(self, file_id: str, updates: Dict[str, Any]) -> None:
        async with self._lock:
            rec = self._records.get(file_id, {})
            rec.update(updates)
            if "created_at" not in rec:
                rec["created_at"] = time.time()
            rec["file_id"] = file_id
            self._records[file_id] = rec
