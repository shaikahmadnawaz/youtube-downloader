from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.audio_downloader import download_audio
from app.services.audio_playlist_downloader import download_playlist
from app.schemas.audio import AudioRequest, AudioResponse

router = APIRouter()

@router.post("/download", response_model=AudioResponse)
async def download_audios(
    request: AudioRequest, background_tasks: BackgroundTasks
):
    """
    Endpoint to download YouTube videos.
    """
    try:
        # Add the download task to the background
        audio_info = await download_audio(request.url, background_tasks)
        return audio_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download/playlist", response_model=AudioResponse)
async def download_playlists(
    request: AudioRequest, background_tasks: BackgroundTasks
):
    """
    Endpoint to download YouTube playlists.
    """
    try:
        # Add the download task to the background
        audio_info = await download_playlist(request.url, background_tasks)
        return audio_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
