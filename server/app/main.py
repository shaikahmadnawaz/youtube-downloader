from fastapi import FastAPI
from app.routes import videos

app = FastAPI(title="YouTube Video Downloader")

app.include_router(videos.router, prefix="/videos", tags=["Videos"])



@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Downloader API!"}
