from pydantic import BaseModel, Field
from typing import Optional


class Statistics(BaseModel):
    viewCount: Optional[int] = Field(default=None)
    likeCount: Optional[int] = Field(default=None)
    dislikeCount: Optional[int] = Field(default=None)
    favoriteCount: Optional[int] = Field(default=None)
    commentCount: Optional[int] = Field(default=None)
