from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    apy_key: str


class Tweet(BaseModel):
    id: int
    content: str
    author_id: int


class Like(BaseModel):
    id: int
    user_id: int
    tweet_id: int


class Media(BaseModel):
    id: int
    tweet_id: int
    url: str


class Follow(BaseModel):
    id: int
    user_id: int
    follower_id: int
