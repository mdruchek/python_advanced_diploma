from typing_extensions import Annotated

from sqlalchemy import Integer, String, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

str50 = Annotated[str, 50]
str500 = Annotated[str, 500]


class Base(DeclarativeBase):
    type_annotation_map = {
        str50: String(50),
        str500: String(500)
    }


class User(Base):
    """Модель User"""
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, Sequence('user_id_seq'), primary_key=True)
    name: Mapped[str50]
    api_key: Mapped[str50]


class Tweet(Base):
    """Модель Tweet"""
    __tablename__ = 'tweet'

    id: Mapped[int] = mapped_column(Integer, Sequence('tweet_id_seq'), primary_key=True)
    content: Mapped[str500]
    author_id: Mapped[int]


class Like(Base):
    """Модель Like"""
    __tablename__ = 'like'

    id: Mapped[int] = mapped_column(Integer, Sequence('like_id_seq'), primary_key=True)
    user_id: Mapped[int]
    tweet_id: Mapped[int]


class Media(Base):
    """Модель Media"""
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(Integer, Sequence('media_id_seq'), primary_key=True)
    tweet_id: Mapped[int]
    url: Mapped[str]


class Follow(Base):
    """Модель Follow"""
    __tablename__ = 'follow'

    id: Mapped[int] = mapped_column(Integer, Sequence('follow_id_seq'), primary_key=True)
    user_id: Mapped[int]
    follower_id: Mapped[int]
