# Mini File Server

A fully asynchronous file server built with FastAPI. It supports uploading files, listing stored files and downloading files. Files are stored in a configurable directory (default `storage/`). This service is designed with modular architecture, uses classes for business logic, and includes comprehensive API documentation.

## Features

- Upload any file asynchronously via POST `/upload`.
- List available files via GET `/files`.
- Download files via GET `/download/{filename}` with streaming to conserve memory.
- Modular architecture separating FastAPI routes (`app/main.py`), service layer (`app/services.py`), and data models (`app/models.py`).
- Uses `aiofiles` for non-blocking file I/O and `pydantic` for data validation.
- Configurable storage directory, easily containerizable.

## Architecture Overview

Project structure:

```
mini_file_server/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # Pydantic schemas for responses
│   └── services.py      # Business logic for file storage
├── storage/             # Directory created at runtime to store uploaded files
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

Modules:

- **app/models.py**: Pydantic models `UploadResponse` and `FileListResponse` used for API responses.
- **app/services.py**: `FileService` class encapsulates file system operations (saving, listing, streaming). It uses `aiofiles` for async I/O and logs actions with `logging`.
- **app/main.py**: Initializes the FastAPI app, configures logging, instantiates `FileService`, and defines API endpoints.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/okaloopen/auto-generated-mini-file-server.git
cd auto-generated-mini-file-server
```

2. Install dependencies (preferably within a virtual environment):

```bash
pip install -r requirements.txt
```

## Running the Server

Start the API with Uvicorn:

```bash
uvicorn app.main:app --reload
```

By default the service stores files under `storage/`. You can configure a different directory by passing an environment variable or modifying the `FileService` initialization in `app/main.py`.

## API Documentation

| Method | Endpoint                | Description                              | Request Body                         | Response                     |
|-------|-------------------------|------------------------------------------|--------------------------------------|-----------------------------|
| GET   | `/health`               | Health check endpoint                    | –                                    | `{"status": "ok"}`         |
| POST  | `/upload`               | Upload a file                            | Multipart file with field `file`     | `{"filename": "<name>"}`   |
| GET   | `/files`                | List all stored files                    | –                                    | `{"files": [list]}`        |
| GET   | `/download/{filename}`  | Download a specific file (streaming)     | –                                    | File content (stream)       |

## Logging

The application uses Python's built-in `logging` module to record informational messages and errors. Logs can be configured further by adjusting the logging configuration in `app/main.py`.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
