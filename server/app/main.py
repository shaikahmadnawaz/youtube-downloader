from fastapi import FastAPI, status
from app.routes import videos
from app.routes import audios

version = "v1"

app = FastAPI(title="YouTube Video Downloader",
description="This is a simple API that allows you to download YouTube videos in different formats.",
version=version,
)

app.include_router(videos.router, prefix=f"/api/{version}/videos", tags=["Videos"], )

app.include_router(audios.router, prefix=f"/api/{version}/audios", tags=["Audios"], )


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome to the YouTube Downloader API!"}