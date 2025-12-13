import csv
from io import StringIO
from collections import defaultdict
from typing import Dict, Any, Tuple, List


async def process_csv(file_content: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Parse CSV content and compute aggregates.\n
    Expects header: sensor_id,timestamp,value
    """
    reader = csv.DictReader(StringIO(file_content))
    row_count = 0
    min_value = float("inf")
    max_value = float("-inf")
    sum_value = 0.0
    per_sensor_count = defaultdict(int)
    errors: List[Dict[str, Any]] = []

    for rowIndex, row in enumerate(reader, start=1):
        try:
            sensor_id = row["sensor_id"]
            value_raw = row["value"]
            value = float(value_raw)
        except KeyError as e:
            errors.append({"row": rowIndex, "error": f"missing column {e}"})
            continue
        except ValueError:
            errors.append({"row": rowIndex, "error": f"invalid float: {row.get('value')}"})
            continue
        except Exception as e:
            errors.append({"row": rowIndex, "error": str(e)})
            continue

        row_count += 1
        sum_value += value
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value
        per_sensor_count[sensor_id] += 1

    mean_value = (sum_value / row_count) if row_count else None

    aggregates = {
        "row_count": row_count,
        "min_value": (min_value if row_count else None),
        "max_value": (max_value if row_count else None),
        "mean_value": mean_value,
        "per_sensor_count": dict(per_sensor_count),
    }

    return aggregates, errors
