import os
import yt_dlp
from fastapi import BackgroundTasks, HTTPException
from pydantic import HttpUrl

async def download_audio(url: HttpUrl, background_tasks: BackgroundTasks):
    """
    Downloads audio from YouTube in high quality using yt-dlp.
    """
    output_dir = "./downloads/audios/"
    os.makedirs(output_dir, exist_ok=True)

    # Options for audio-only download
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),  # Save location
        "format": "bestaudio/best",  # Download best audio available
        "postprocessors": [
            {  # Extract audio and convert to MP3
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",  # Output format (e.g., mp3)
                "preferredquality": "320",  # Bitrate (can be adjusted: 128, 192, 320)
            }
        ],
    }

    def download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                url_str = str(url)  # Convert HttpUrl to string
                info = ydl.extract_info(url_str, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", ".mp3")  # Update filename extension
                print(f"Audio download complete: {filename}")
        except Exception as e:
            print(f"Error downloading audio: {e}")

    # Add download to background task
    background_tasks.add_task(download)
    return {"message": "Audio download started in high quality!", "url": url}
