import pytest
from app.services.processor import process_csv


@pytest.mark.asyncio
async def test_processor_basic():
    csv_data = "sensor_id,timestamp,value\nsensor-A,2025-10-01T08:12:03Z,23.5\nsensor-B,2025-10-01T08:12:07Z,19.87"
    aggregates, errors = await process_csv(csv_data)
    assert aggregates["row_count"] == 2
    assert aggregates["min_value"] == 19.87
    assert aggregates["max_value"] == 23.5
    assert aggregates["per_sensor_count"]["sensor-A"] == 1
    assert aggregates["per_sensor_count"]["sensor-B"] == 1
    assert errors == []

@pytest.mark.asyncio
async def test_processor_invalid_fload():
    csv_data = "sensor_id,timestamp,value\nsensor-A,2025-10-01T08:12:03Z,23.5\nsensor-B,2025-10-01T08:12:07Z,not_a_number"
    aggregates, errors = await process_csv(csv_data)
    assert aggregates["row_count"] == 1
    assert aggregates["min_value"] == 23.5
    assert aggregates["max_value"] == 23.5
    assert aggregates["per_sensor_count"]["sensor-A"] == 1
    assert "senson-B" not in aggregates["per_sensor_count"]
    
    assert len(errors) == 1
    assert errors[0]["row"] == 2
    assert "invalid float: not_a_number" in errors[0]["error"]
