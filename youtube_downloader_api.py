from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import yt_dlp
import os
import uuid
import shutil

app = FastAPI()

DOWNLOAD_DIR = "downloads"
COOKIES_FILE = "cookies.txt"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

@app.post("/api/download")
def download_video(request: DownloadRequest):
    video_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
    ydl_opts = {
        'outtmpl': output_template,
        'cookiefile': COOKIES_FILE,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            ext = info.get('ext', 'mp4')
            filename = f"{video_id}.{ext}"
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            if not os.path.exists(filepath):
                # fallback: try to find the file
                for f in os.listdir(DOWNLOAD_DIR):
                    if f.startswith(video_id):
                        filepath = os.path.join(DOWNLOAD_DIR, f)
                        break
            return {"video_id": video_id, "filename": os.path.basename(filepath), "title": info.get('title'), "status": "downloaded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/videos/{video_id}")
def get_video_details(video_id: str):
    # Find the file by video_id
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(video_id):
            filepath = os.path.join(DOWNLOAD_DIR, f)
            # Try to extract info from filename
            return {"video_id": video_id, "filename": f, "path": filepath}
    raise HTTPException(status_code=404, detail="Video not found")

@app.get("/api/videos/{video_id}/download")
def download_video_file(video_id: str):
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(video_id):
            filepath = os.path.join(DOWNLOAD_DIR, f)
            return FileResponse(filepath, filename=f)
    raise HTTPException(status_code=404, detail="Video not found")
