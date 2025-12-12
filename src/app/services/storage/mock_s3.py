from typing import Dict, Optional
import asyncio

from src.app.services.storage.storage_interface import FileStorage


class MockS3(FileStorage):
    def __init__(self) -> None:
        self._files: Dict[str, str] = {}
        self._lock = asyncio.Lock()

    async def upload_file(self, file_id: str, content: str) -> None:
        async with self._lock:
            self._files[file_id] = content

    async def get_file(self, file_id: str) -> Optional[str]:
        async with self._lock:
            return self._files.get(file_id)
