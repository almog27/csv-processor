# CSV Processor Task
## Almog Ben David

### Explanation

In a big tasks I try to create a design document that will help me to plan my steps, understand the requirements and the desired architecture, before starting to work.
This helps me to understand what are the open questions in advance and the possible things that we will takle them later, and raise them as early as possible.

### Overview - The Problem & Requirements

CSV Processor is a Python-based system responsible for:
* Accepting CSV file containing sensor readings
* Upload each file to store object (mocked)
* Aggregating values and counting rows per sensor
* Recording the results in a cloud database (mocked)
* Providing HTTP API (FastAPI)
* Simplify the usage of the solution (Makefile, Docker)
* Considering a scalable, cloud-ready architecture
* Optional - CLI interface
* Optional - Frontend interface

### Architecture

The system will be composed of the next components:
1. Backend service (FastAPI) - the primary API service
2. Storage Manager - Factory for many storage solutions, will help us replacing mock with real storage solutions, or replace with storage solutions
3. CSV Processor - the actual processing part
4. Async in-memory Queue - job queue for scale
5. Worker for consuming the queue
6. CLI tool - 
7. React UI - presenting the results and the files

### Diagram
Web UI 
=> 
Backend Service + CLI
=>
StorageManager
=>
S3 Storage / DB Storage
<=
Async file queue
=>
Worker processing file

### Functional Requirements

1. Upload CSV file
* Accept file via API (or CLI)
* Store the file in storage (S3)
* Create metadata entry in storage (DB)
* Send the file to queue for background processing
* Returns the file id for tracking abilities

2. CSV Parsing and Validation
* row structure -> sensor_id, timestamp, value
* invalid rows should not stop processing, should affect the status

3. Aggregation requirements
* Keep for each file - the row_count, min_value, max_value and per_sensor_count

4. Metadata
* We should keep in the storage DB: file_id, upload time, processing duration (ms), proceesing status, the aggreagations and list of invalid rows

### Data Model

Data stored per file in the DB storage
```
{
    file_id: number,
    status: "processed" | "partial" | "failed" | "waiting",
    upload_time: timestamp,
    aggregations: {
        "row_count: number,
        "min_value": number,
        "max_value": number,
        "per_sensor_count": {
            sensor_name: value
        }
    },
    invalid_rows: [
        {
            row: number,
            error: string
        }
    ]
}
```

### Error Handling

1. API validations
    1. Missing file - API returns 400 Bad Request: Missing file
    2. Wrong file type - API returns 400 Bad Request: Invalid Parameter Type
2. CSV parsing - invalid rows -> saved in the metadata
3. Storage error - "failed" status in metadata
4. Worker error - "failed" status in metadata

### Future thoughts

1. Supporting caching using redis for results
2. Authentication support
3. UI improvments - pagination
4. UI - real results
