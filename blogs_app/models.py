from typing_extensions import Annotated

from sqlalchemy import Integer, String, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


required_str = Annotated[str, mapped_column(String, nullable=False)]
required_str50 = Annotated[str, mapped_column(String(50), nullable=False)]
required_str500 = Annotated[str, mapped_column(String(500), nullable=False)]


class Base(DeclarativeBase):
    pass


class User(Base):
    """Модель User"""
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, Sequence('user_id_seq'))
    name: Mapped[required_str50]
    api_key: Mapped[required_str50]


class Tweet(Base):
    """Модель Tweet"""
    __tablename__ = 'tweet'

    id: Mapped[int] = mapped_column(Integer, Sequence('tweet_id_seq'), primary_key=True)
    content: Mapped[required_str500]
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
    url: Mapped[required_str]


class Follow(Base):
    """Модель Follow"""
    __tablename__ = 'follow'

    id: Mapped[int] = mapped_column(Integer, Sequence('follow_id_seq'), primary_key=True)
    user_id: Mapped[int]
    follower_id: Mapped[int]
