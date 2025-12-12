from typing import Protocol, runtime_checkable, Dict, Any, Optional


@runtime_checkable
class FileStorage(Protocol):
    async def upload_file(self, file_id: str, content: str) -> None: ...

    async def get_file(self, file_id: str) -> Optional[str]: ...


@runtime_checkable
class MetadataStore(Protocol):
    async def insert_file_record(self, file_id: str, record: Dict[str, Any]) -> None: ...

    async def get_file_record(self, file_id: str) -> Optional[Dict[str, Any]]: ...

    async def update_file_record(self, file_id: str, updates: Dict[str, Any]) -> None: ...
