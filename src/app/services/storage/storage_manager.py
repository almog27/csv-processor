import time
from typing import Dict, Any

from .storage_interface import FileStorage, MetadataStore


# Storage Manager
# Responsible for all the storagre operations in the service
# Has two storage types - File (S3 like) and Metadata (DB like)
# Those can be replaced easily by any other wrapper
class StorageManager:
    def __init__(self, file_storage: FileStorage, metadata_store: MetadataStore):
        if not isinstance(file_storage, FileStorage):
            raise TypeError("file_storage must implement FileStorage protocol")

        if not isinstance(metadata_store, MetadataStore):
            raise TypeError("metadata_store must implement MetadataStore protocol")

        self.file_storage = file_storage
        self.metadata_store = metadata_store

    async def upload_file(self, file_id: str, content: str) -> None:
        await self.file_storage.upload_file(file_id, content)

        record: Dict[str, Any] = {
            "file_id": file_id,
            "status": "queued",
            "created_at": time.time(),
            "aggregates": None,
            "errors": [],
        }

        await self.metadata_store.insert_file_record(file_id, record)

    async def get_file(self, file_id: str):
        return await self.file_storage.get_file(file_id)

    async def get_file_record(self, file_id: str):
        return await self.metadata_store.get_file_record(file_id)

    async def update_file_record(self, file_id: str, updates: Dict[str, Any]):
        await self.metadata_store.update_file_record(file_id, updates)
