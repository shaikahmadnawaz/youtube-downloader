import os
import yt_dlp
from fastapi import BackgroundTasks, HTTPException
from pydantic import HttpUrl

async def download_video(url: HttpUrl, background_tasks: BackgroundTasks):
    """
    Downloads a video from YouTube in high quality using yt-dlp and merges streams.
    """
    output_dir = "./downloads/videos/"
    os.makedirs(output_dir, exist_ok=True)

    # High-quality video and audio with merging
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),  # Save location
        "format": "bestvideo+bestaudio",  # Download best video and audio streams
        "postprocessors": [
            {  # Merge audio and video using FFmpeg
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # Output format
            }
        ],
    }

    def download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                url_str = str(url)  # Convert HttpUrl to string
                info = ydl.extract_info(url_str, download=True)
                filename = ydl.prepare_filename(info)
                print(f"Download complete: {filename}")
        except Exception as e:
            print(f"Error downloading video: {e}")

    # Add download to background task
    background_tasks.add_task(download)
    return {"message": "Download started at high quality!", "url": url}
