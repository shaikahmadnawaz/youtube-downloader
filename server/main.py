from fastapi import FastAPI

app = FastAPI(title="YouTube Downloader API")

@app.get("/")
async def read_root():
    return {"message": "Welcome to YouTube Downloader API!"}