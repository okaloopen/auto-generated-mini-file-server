from __future__ import annotations

import os
import logging
from typing import List, AsyncIterator

import aiofiles

logger = logging.getLogger(__name__)

class FileService:
    """Service for saving, listing and streaming files asynchronously."""

    def __init__(self, upload_dir: str = "uploads") -> None:
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, filename: str, file) -> str:
        """Save an uploaded file asynchronously and return its path."""
        file_path = os.path.join(self.upload_dir, filename)
        logger.info("Saving file %s", file_path)
        async with aiofiles.open(file_path, "wb") as out_file:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                await out_file.write(chunk)
        return file_path

    async def list_files(self) -> List[str]:
        """Return a list of filenames available in the upload directory."""
        logger.info("Listing files in %s", self.upload_dir)
        return [f for f in os.listdir(self.upload_dir) if os.path.isfile(os.path.join(self.upload_dir, f))]

    async def stream_file(self, filename: str) -> AsyncIterator[bytes]:
        """Asynchronously read file in chunks for streaming."""
        file_path = os.path.join(self.upload_dir, filename)
        logger.info("Streaming file %s", file_path)
        if not os.path.exists(file_path):
            return

        async with aiofiles.open(file_path, "rb") as f:
            while True:
                chunk = await f.read(1024 * 64)
                if not chunk:
                    break
                yield chunk
