import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, storage
from app.services.processor import process_csv


@pytest.mark.asyncio
async def test_upload_and_results():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        csv_data = "sensor_id,timestamp,value\nsensor-A,2025-10-01T08:12:03Z,23.5\n"
        resp = await client.post("/upload", files={"file": ("file.csv", csv_data)})
        assert resp.status_code == 200
        file_id = resp.json()["file_id"]

        # Trigger processing manually because test can't rely on running worker on startup
        content = await storage.get_file(file_id)
        assert content is not None

        # simulate processing
        aggregates, errors = await process_csv(content)
        await storage.update_file_record(
            file_id,
            {
                "status": "processed" if not errors else "partial",
                "aggregates": aggregates,
                "errors": errors,
                "duration_ms": 0,
            },
        )

        # now get results via API
        resp2 = await client.get(f"/results/{file_id}")
        assert resp2.status_code == 200
        data = resp2.json()
        assert data["aggregates"]["row_count"] == 1
