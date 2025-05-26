#!/usr/bin/env python3
import os
import re
import argparse
from yt_dlp import YoutubeDL

COOKIES_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cookies.txt'))
DOWNLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'downloads'))

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

def sanitize_filename(title):
    title = re.sub(r'[\\/*?:"<>|]', '_', title)
    title = re.sub(r'[^\x00-\x7F]+', '', title)
    return title.strip()

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo[height<=480][ext=mp4]/bestvideo[ext=mp4]/best',
        'quiet': False,
        'cookiefile': COOKIES_FILE
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'title' in info and isinstance(info['title'], str):
            sanitized_title = sanitize_filename(info['title'])
            video_path = os.path.join(DOWNLOADS_DIR, f"{sanitized_title}.mp4")
            if not os.path.exists(video_path):
                ydl_opts['outtmpl'] = video_path
                with YoutubeDL(ydl_opts) as ydl_download:
                    ydl_download.download([url])
                print(f"Downloaded: {video_path}")
            else:
                print(f"Video already exists: {video_path}")
        else:
            print("Error: 'title' not found or not a string in info.")
            return None
    return video_path

def main():
    parser = argparse.ArgumentParser(description='Download a YouTube video using yt-dlp and cookies.txt')
    parser.add_argument('url', help='YouTube video URL')
    args = parser.parse_args()
    download_youtube_video(args.url)

if __name__ == '__main__':
    main()
