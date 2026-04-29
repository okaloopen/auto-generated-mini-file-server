from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    filename: str

class FileListResponse(BaseModel):
    files: List[str]
