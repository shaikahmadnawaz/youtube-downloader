from pydantic import BaseModel, HttpUrl

class AudioRequest(BaseModel):
    url: HttpUrl

class AudioResponse(BaseModel):
    message: str
    url: HttpUrl
