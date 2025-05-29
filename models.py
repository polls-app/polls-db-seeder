from datetime import datetime

from sqlalchemy import (
    String, Text, Boolean, DateTime, Enum, SmallInteger,
    CHAR, ForeignKey, UUID, Enum, Integer, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from pgvector.sqlalchemy import Vector


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(97))
    role: Mapped[str] = mapped_column(
        Enum("pollee", "admin", name="user_roles")
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")
    polls: Mapped[list["Poll"]] = relationship("Poll", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    username: Mapped[str] = mapped_column(String(37), unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(Text)
    avatar_path: Mapped[str | None] = mapped_column(String(255))
    contribution_count: Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    polls: Mapped[list["Poll"]] = relationship("Poll", back_populates="category")


class Hashtag(Base):
    __tablename__ = "hashtags"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(20))


class HashtagToPoll(Base):
    __tablename__ = "hashtags_to_polls"

    hashtag_id: Mapped[str] = mapped_column(UUID, ForeignKey("hashtags.id"), primary_key=True)
    poll_id: Mapped[str] = mapped_column(UUID, ForeignKey("polls.id"), primary_key=True)


class Poll(Base):
    __tablename__ = "polls"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    possible_answers_count: Mapped[int] = mapped_column(SmallInteger, default=1)
    color_hex: Mapped[str] = mapped_column(CHAR(7))
    lang_code: Mapped[str] = mapped_column(CHAR(2))
    access_mode: Mapped[str] = mapped_column(
        Enum("public", "restricted", name="poll_access_modes")
    )
    embedding: Mapped[list[float]] = mapped_column(Vector(830))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"))
    category_id: Mapped[str] = mapped_column(UUID, ForeignKey("categories.id"))

    user: Mapped["User"] = relationship("User", back_populates="polls")
    category: Mapped["Category"] = relationship("Category", back_populates="polls")
    options: Mapped[list["Option"]] = relationship("Option", back_populates="poll")


class Option(Base):
    __tablename__ = "options"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    content: Mapped[str] = mapped_column(String(40))
    position: Mapped[int] = mapped_column(SmallInteger)
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    poll_id: Mapped[str] = mapped_column(UUID, ForeignKey("polls.id"))

    poll: Mapped["Poll"] = relationship("Poll", back_populates="options")


class Vote(Base):
    __tablename__ = "votes"

    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"), primary_key=True)
    option_id: Mapped[str] = mapped_column(UUID, ForeignKey("options.id"), primary_key=True)
    voted_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


class Share(Base):
    __tablename__ = "shares"

    user_id: Mapped[str] = mapped_column(UUID, primary_key=True)
    poll_id: Mapped[str] = mapped_column(UUID, primary_key=True)


class Following(Base):
    __tablename__ = "followings"

    follower_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"), primary_key=True)
    followed_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id])
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])


class PollInvitedUser(Base):
    __tablename__ = "poll_invited_users"

    poll_id: Mapped[str] = mapped_column(UUID, ForeignKey("polls.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"), primary_key=True)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    content: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)
    parent_id: Mapped[str | None] = mapped_column(UUID, ForeignKey("comments.id"))
    poll_id: Mapped[str] = mapped_column(UUID, ForeignKey("polls.id"))
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey("users.id"))

    poll: Mapped["Poll"] = relationship("Poll")
    user: Mapped["User"] = relationship("User")
