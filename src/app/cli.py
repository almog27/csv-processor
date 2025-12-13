import asyncio
from pathlib import Path
import typer
from uuid import uuid4

from src.app.services.storage.storage_manager import StorageManager
from src.app.services.storage.mock_s3 import MockS3
from src.app.services.storage.mock_db import MockDB
from src.app.services.queue_manager import enqueue_file
from src.app.services.processor import process_csv

app = typer.Typer()
storage = StorageManager(file_storage=MockS3(), metadata_store=MockDB())


@app.command()
def upload(file: str):
    """
    Upload a CSV file to storage and enqueue for processing.
    """
    p = Path(file)
    if not p.exists():
        typer.echo(f"file {file} not found")
        raise typer.Exit(code=1)

    content = p.read_text()
    file_id = str(uuid4())

    async def _run():
        await storage.upload_file(file_id, content)
        await enqueue_file(file_id)
        typer.echo(f"uploaded and enqueued file_id: {file_id}")

    asyncio.run(_run())


@app.command()
def process(file_id: str, file: str):
    """
    Force processing of a local file and store results under file_id (synchronous CLI).
    """
    p = Path(file)
    if not p.exists():
        typer.echo(f"file {file} not found")
        raise typer.Exit(code=1)

    content = p.read_text()

    async def _run():
        aggregates, errors = await process_csv(content)
        status = "processed" if not errors else "partial"
        await storage.update_file_record(
            file_id,
            {
                "status": status,
                "aggregates": aggregates,
                "errors": errors,
            },
        )
        typer.echo(f"processed {file_id} (status: {status})")
        typer.echo(f"aggregates: {aggregates}")
        if errors:
            typer.echo(f"errors: {errors}")

    asyncio.run(_run())


@app.command()
def results(file_id: str):
    """
    Print processing results for file_id.
    """
    async def _run():
        rec = await storage.get_file_record(file_id)
        if not rec:
            typer.echo("not found")
            raise typer.Exit(code=1)
        typer.echo(rec)

    asyncio.run(_run())


if __name__ == "__main__":
    app()
