__all__ = (
    'User',
    'Category',
    'File'
)

from datetime import datetime
from typing import Optional, List

from core.database.base import Base
from sqlalchemy import BigInteger, ForeignKey, func, DateTime, Identity
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from core.domain.file import FileType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f'<User id={self.id!r} created_at={self.created_at!r} deleted_at={self.deleted_at!r}'


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user: Mapped[User] = relationship()

    title: Mapped[str]
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    files: Mapped[List["File"]] = relationship(lazy="noload")


class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    remote_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user: Mapped["User"] = relationship()

    type_id: Mapped[FileType]

    category_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("categories.id"))
    category: Mapped[Optional[Category]] = relationship()

    title: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
