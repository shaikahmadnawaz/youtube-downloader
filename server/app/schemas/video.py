from pydantic import BaseModel, HttpUrl

class VideoRequest(BaseModel):
    url: HttpUrl

class VideoResponse(BaseModel):
    message: str
    url: HttpUrl
