from typing_extensions import Annotated

from sqlalchemy import Integer, String, Sequence, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


required_str = Annotated[str, mapped_column(String, nullable=False)]
required_str50 = Annotated[str, mapped_column(String(50), nullable=False)]
required_str500 = Annotated[str, mapped_column(String(500), nullable=False)]


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Модель User

    Attributes:
        id (int): первичный ключ
        name (str): имя пользователя
        api_key (str): api_key пользователя

    Methods:
        to_dict: преобразование экземпляра модели в словарь
    """

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
    follows_author: Mapped[list['Follow']] = relationship(back_populates='author', foreign_keys='[Follow.author_id]')
    follows_follower: Mapped[list['Follow']] = relationship(back_populates='follower', foreign_keys='[Follow.follower_id]')

    def to_dict(self, exclude=()):
        """
        Преобразование модели в словарь

        :param exclude: поля модели исключить из возвращенного словаря
        :type exclude: tuple

        :return: словарь атрибутов модели
        :rtype: dict
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude}


class Tweet(Base):
    """
    Модель Tweet

    Attributes:
        id (int): первичный ключ
        content (str): содержание твита
        author_id (int): id автора
        media_ids (json): id медиафайлов

    Methods:
    to_dict: преобразование экземпляра модели в словарь
    """

    __tablename__ = 'tweet'

    id: Mapped[int] = mapped_column(Integer, Sequence('tweet_id_seq'), primary_key=True)
    content: Mapped[required_str500]
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    # создать миграцию
    media_ids = mapped_column(JSON)

    author: Mapped['User'] = relationship(back_populates='tweets')
    likes: Mapped[list['Like']] = relationship(
        back_populates='tweet',
        cascade='all, delete',
        passive_deletes=True,
    )
    # medias: Mapped[list['Media']] = relationship(
    #     back_populates='tweet',
    #     cascade='all, delete',
    #     passive_deletes=True,
    # )

    def to_dict(self):
        """
        Преобразование модели в словарь

        :return: словарь атрибутов модели
        :rtype: dict
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Like(Base):
    """
    Модель Like

    Attributes:
        id (int): первичный ключ
        user_id (int): id пользователя
        tweet_id (int): id твита

    Methods:
        to_dict: преобразование экземпляра модели в словарь
    """

    __tablename__ = 'like'
    __table_args__ = (
        #создать миграцию
        UniqueConstraint('user_id', 'tweet_id'),
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('like_id_seq'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'))
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweet.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='likes')
    tweet: Mapped['Tweet'] = relationship(back_populates='likes')

    def to_dict(self):
        """
        Преобразование модели в словарь

        :return: словарь атрибутов модели
        :rtype: dict
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Media(Base):
    """
    Модель Media

    Attributes:
        id (int): первичный ключ
        url (str): url медиафайла

    Methods:
        to_dict: преобразование экземпляра модели в словарь
    """

    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(Integer, Sequence('media_id_seq'), primary_key=True)
    # создать миграцию
    # tweet_id: Mapped[int] = mapped_column(ForeignKey('tweet.id', ondelete='CASCADE'))
    url: Mapped[required_str]

    # tweet: Mapped['Tweet'] = relationship(back_populates='medias')

    def to_dict(self):
        """
        Преобразование модели в словарь

        :return: словарь атрибутов модели
        :rtype: dict
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Follow(Base):
    """
    Модель Follow

    Attributes:
        id (str): первичный ключ
        author_id (str): id автора
        follower_id (str): id подписчика

    Methods:
        to_dict: преобразование экземпляра модели в словарь
    """

    __tablename__ = 'follow'
    __table_args__ = (
        #создать миграцию
        UniqueConstraint('author_id', 'follower_id'),
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('follow_id_seq'), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    author: Mapped['User'] = relationship(foreign_keys=[author_id])
    follower: Mapped['User'] = relationship(foreign_keys=[follower_id])

    def to_dict(self):
        """
        Преобразование модели в словарь

        :return: словарь атрибутов модели
        :rtype: dict
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
