from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    api_key: str


class TweetSchema(BaseModel):
    id: int
    content: str
    author_id: int


class LikeSchema(BaseModel):
    id: int
    user_id: int
    tweet_id: int


class MediaSchema(BaseModel):
    id: int
    tweet_id: int
    url: str


class FollowSchema(BaseModel):
    id: int
    author_id: int
    follower_id: int
