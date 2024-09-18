from typing_extensions import Annotated

from sqlalchemy import Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


required_str = Annotated[str, mapped_column(String, nullable=False)]
required_str50 = Annotated[str, mapped_column(String(50), nullable=False)]
required_str500 = Annotated[str, mapped_column(String(500), nullable=False)]


class Base(DeclarativeBase):
    pass


class User(Base):
    """Модель User"""
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, Sequence('user_id_seq'), primary_key=True)
    name: Mapped[required_str50]
    # создать миграцию
    api_key: Mapped[required_str50] = mapped_column(unique=True)

    tweets: Mapped[list['Tweet']] = relationship(
        back_populates='author',
        cascade='all, delete',
        passive_deletes=True,
    )
    likes: Mapped[list['Like']] = relationship(back_populates='user')
    follow_authors: Mapped[list['Follow']] = relationship(back_populates='author')
    follow_followers: Mapped[list['Follow']] = relationship(back_populates='follower')


class Tweet(Base):
    """Модель Tweet"""
    __tablename__ = 'tweet'

    id: Mapped[int] = mapped_column(Integer, Sequence('tweet_id_seq'), primary_key=True)
    content: Mapped[required_str500]
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    author: Mapped['User'] = relationship(back_populates='tweets')
    likes: Mapped[list['Like']] = relationship(
        back_populates='tweet',
        cascade='all, delete',
        passive_deletes=True,
    )
    medias: Mapped[list['Media']] = relationship(
        back_populates='tweet',
        cascade='all, delete',
        passive_deletes=True,
    )


class Like(Base):
    """Модель Like"""
    __tablename__ = 'like'

    id: Mapped[int] = mapped_column(Integer, Sequence('like_id_seq'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'))
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweet.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='likes')
    tweet: Mapped['Tweet'] = relationship(back_populates='likes')


class Media(Base):
    """Модель Media"""
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(Integer, Sequence('media_id_seq'), primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweet.id', ondelete='CASCADE'))
    url: Mapped[required_str]

    tweet: Mapped['Tweet'] = relationship(back_populates='medias')


class Follow(Base):
    """Модель Follow"""
    __tablename__ = 'follow'

    id: Mapped[int] = mapped_column(Integer, Sequence('follow_id_seq'), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    author: Mapped['User'] = relationship(back_populates='author', foreign_keys=[author_id])
    follower: Mapped['User'] = relationship(back_populates='follower', foreign_keys=[follower_id])
