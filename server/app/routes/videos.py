from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.downloader import download_video
from app.schemas.video import VideoRequest, VideoResponse

router = APIRouter()

@router.post("/download", response_model=VideoResponse)
async def download_videos(
    request: VideoRequest, background_tasks: BackgroundTasks
):
    """
    Endpoint to download YouTube videos.
    """
    try:
        # Add the download task to the background
        video_info = await download_video(request.url, background_tasks)
        return video_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
