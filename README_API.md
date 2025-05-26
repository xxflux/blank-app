# How to run the FastAPI YouTube Downloader API

## Install dependencies

```bash
pip3 install -r requirements-api.txt
```

## Start the API server

```bash
uvicorn youtube_downloader_api:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Download Video
- **POST** `/api/download`
- **Body:** `{ "url": "<youtube_url>" }`
- **Response:** `{ "video_id": "...", "filename": "...", "title": "...", "status": "downloaded" }`

### Get Video Details
- **GET** `/api/videos/{video_id}`
- **Response:** `{ "video_id": "...", "filename": "...", "path": "..." }`

### Download Video File
- **GET** `/api/videos/{video_id}/download`
- **Response:** Returns the video file for download.

## Notes
- The API uses `cookies.txt` in the root directory for authentication.
- Downloaded videos are stored in the `downloads/` directory.
- The API uses the latest `yt-dlp` for downloading videos.
