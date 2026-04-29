from __future__ import annotations

import logging
from typing import AsyncIterator

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from starlette.status import HTTP_201_CREATED

from .services import FileService
from .models import UploadResponse, FileListResponse

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mini File Server",
    description="Asynchronous file server with upload and download capabilities.",
    version="0.1.0",
)

file_service = FileService()

@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/upload", response_model=UploadResponse, status_code=HTTP_201_CREATED)
async def upload_file(file: UploadFile) -> UploadResponse:
    """Handle file upload and return saved path."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    saved_path = await file_service.save_file(file.filename, file.file)
    return UploadResponse(filename=file.filename, path=saved_path)

@app.get("/files", response_model=FileListResponse)
async def list_files() -> FileListResponse:
    """Return a list of available files."""
    files = await file_service.list_files()
    return FileListResponse(files=files)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Stream a file to the client if it exists."""
    stream = file_service.stream_file(filename)
    if stream is None:
        raise HTTPException(status_code=404, detail="File not found")

    async def file_iterator() -> AsyncIterator[bytes]:
        async for chunk in stream:
            yield chunk

    return StreamingResponse(
        file_iterator(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename=\"{filename}\"'},
    )
