import pytest
from app.services.storage.mock_s3 import MockS3
from app.services.storage.mock_db import MockDB
from app.services.storage.storage_manager import StorageManager


@pytest.mark.asyncio
async def test_mock_s3_and_db():
    s3 = MockS3()
    db = MockDB()
    sm = StorageManager(file_storage=s3, metadata_store=db)

    await sm.upload_file("f1", "sensor-A,ts,1.0\n")
    content = await sm.get_file("f1")
    assert "sensor-A" in content

    rec = await sm.get_file_record("f1")
    assert rec is not None
    assert rec["status"] == "queued"

    await sm.update_file_record("f1", {"status": "processed"})
    rec2 = await sm.get_file_record("f1")
    assert rec2["status"] == "processed"
