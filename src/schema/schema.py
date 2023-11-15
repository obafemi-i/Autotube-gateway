from pydantic import BaseModel
from pydantic.networks import NameEmail


class Video(BaseModel):
    to_notify: str
    additional_message: str | None = None
