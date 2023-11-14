from pydantic import BaseModel
from pydantic.networks import NameEmail

class Video(BaseModel):
    video_name: str
    to_notify: NameEmail
    additional_message: str | None = None


