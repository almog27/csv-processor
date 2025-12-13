import asyncio
import time
from typing import Optional, Any

from app.services.processor import process_csv

_storage: Optional[Any] = None

_file_queue: asyncio.Queue = asyncio.Queue()


def init_queue(storage):
    """
    Initialize module with StorageManager instance.\n
    Call once (main) before enqueueing.
    """
    global _storage
    _storage = storage


async def enqueue_file(file_id: str):
    await _file_queue.put(file_id)


async def _process_and_store(file_id: str):
    if _storage is None:
        raise RuntimeError("queue_manager not initialized")

    # get file content from file storage
    content = await _storage.get_file(file_id)
    if content is None:
        # mark failed
        await _storage.update_file_record(
            file_id, {"status": "failed", "errors": [f"file {file_id} not found in object storage"], "duration_ms": 0}
        )
        return

    start = time.time()
    aggregates, errors = await process_csv(content)
    duration_ms = int((time.time() - start) * 1000)
    status = "processed" if not errors else "partial"

    await _storage.update_file_record(
        file_id, {"status": status, "aggregates": aggregates, "errors": errors, "duration_ms": duration_ms}
    )


async def worker():
    while True:
        file_id = await _file_queue.get()
        try:
            await _process_and_store(file_id)
            print(f"[worker] processed {file_id}")
        except Exception as e:
            print(f"[worker] error processing {file_id}: {e}")
            if _storage:
                await _storage.update_file_record(file_id, {"status": "failed", "errors": [str(e)], "duration_ms": 0})
        finally:
            _file_queue.task_done()


def start_workers(n: int = 1):
    loop = asyncio.get_event_loop()
    for _ in range(n):
        loop.create_task(worker())
