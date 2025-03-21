from pydantic import BaseModel
from typing import Literal
from .region_restriction import RegionRestriction
from .content_rating import ContentRating
from .status import Status


class ContentDetails(BaseModel):
    duration: str
    dimension: str
    definition: Literal["hd", "sd"]
    definition: Literal["false", "true"]
    licensedContent: bool
    regionRestriction: RegionRestriction
    duration: str
    contentRating: ContentRating
    projection: Literal["360", "rectangular"]
    status: Status
