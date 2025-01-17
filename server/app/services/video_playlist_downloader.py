import os
import yt_dlp
from fastapi import BackgroundTasks, HTTPException
from pydantic import HttpUrl

async def download_playlist(url: HttpUrl, background_tasks: BackgroundTasks):
    """
    Downloads an entire YouTube playlist in high quality using yt-dlp.
    """
    output_dir = "./downloads/videos/"
    os.makedirs(output_dir, exist_ok=True)

    # High-quality video and audio with merging
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"),  # Save each video in a folder named after the playlist
        "format": "bestvideo+bestaudio",  # Download best video and audio streams
        "postprocessors": [
            {  # Merge audio and video using FFmpeg
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # Output format
            }
        ],
        "noplaylist": False,  # Ensure the entire playlist is downloaded
        "playlistend": None,  # Download all videos (can limit to a number)
    }

    def download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                url_str = str(url)  # Convert HttpUrl to string
                info = ydl.extract_info(url_str, download=True)
                print(f"Playlist download complete: {info.get('title')}")
        except Exception as e:
            print(f"Error downloading playlist: {e}")

    # Add download to background task
    background_tasks.add_task(download)
    return {"message": "Playlist download started!", "url": url}
