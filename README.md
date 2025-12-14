# CSV Processor

A CSV processor service using FastAPI with async queue workers.
It also has CLI support and a UI layer that uses the FastAPI layer.
It processes sensor data from CSV files and computes aggregate metadata.

## Features
**REST API** - Upload CSV file and retrieve processing results
**Async queue** - Processing the aggregation calculations in a queue for scale future support - not waiting for the whole calculations to end
**CLI** - Command line interface support
**Docker support** - Including containerized deployment
**UI** - Simple UI to upload file and get results
**Makefile** for simple use

## CSV Format
According to the instructions, expected CSV format with columns: 'sensor_id', 'timestamp', 'value'
```csv
sensor_id,timestamp,value
sensor-A,2025-10-01T08:12:03Z,23.5
sensor-B,2025-10-01T08:12:07Z,19.87
```

## Setup
```bash
# Create Virtual Environment
make prepare
source .venv/bin/activate

# Install dependences
make install
```

## Usage
### API

```bash
#Start server
make run
```

**Swagger**: http://localhost:2701/docs


**ReDoct**: http://localhost:2701/redoc

**CURL commands**
```bash
# Upload a CSV file
curl -X POST -F "file=@examples/file1.csv" http://localhost:2701/upload

# Show Results
curl http://localhost:2701/results/(file_id)
```

### CLI
```bash
# Process a file and see results
python -m src.app.cli process <file_id> <path_to_csv>

# Or use make
make cli-process FILE_ID=file1 FILE=examples/file1.csv
```

### UI

```bash
# Install frontend dependencies
make ui-prep

# Start the frontend dev server (Vite)
make ui-run
```

**Frontend UI page**: http://localhost:5173

## Development

```bash
# Run tests
make test

# Run Lint
make lint

# Run format code
make fmt
```

## Docker

```bash
# Build and run
make docker-build
make docker-up

# Run tests in container
make docker-test

# Stop and cleanup
make docker-down
```