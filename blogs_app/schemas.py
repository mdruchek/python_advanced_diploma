from pydantic import BaseModel


class UserSchemas(BaseModel):
    id: int
    name: str
    apy_key: str


class TweetSchemas(BaseModel):
    id: int
    content: str
    author_id: int


class LikeSchemas(BaseModel):
    id: int
    user_id: int
    tweet_id: int


class MediaSchemas(BaseModel):
    id: int
    tweet_id: int
    url: str


class FollowSchemas(BaseModel):
    id: int
    author_id: int
    follower_id: int
