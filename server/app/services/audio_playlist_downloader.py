import os
import yt_dlp
from fastapi import BackgroundTasks, HTTPException
from pydantic import HttpUrl

async def download_playlist(url: HttpUrl, background_tasks: BackgroundTasks):
    """
    Downloads an entire YouTube playlist as audio-only files in high quality using yt-dlp.
    """
    output_dir = "./downloads/audios/"
    os.makedirs(output_dir, exist_ok=True)

    # Options for audio-only playlist download
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"),  # Save in playlist folder
        "format": "bestaudio/best",  # Download best audio available
        "postprocessors": [
            {  # Extract audio and convert to MP3
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",  # Output format (e.g., mp3)
                "preferredquality": "320",  # Bitrate (adjustable: 128, 192, 320)
            }
        ],
        "noplaylist": False,  # Ensure the entire playlist is downloaded
        "playlistend": None,  # Download all tracks in the playlist
    }

    def download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                url_str = str(url)  # Convert HttpUrl to string
                info = ydl.extract_info(url_str, download=True)
                playlist_title = info.get("title", "Playlist")
                print(f"Playlist download complete: {playlist_title}")
        except Exception as e:
            print(f"Error downloading playlist: {e}")

    # Add download to background task
    background_tasks.add_task(download)
    return {"message": "Audio playlist download started in high quality!", "url": url}
