__all__ = (
    'User',
    'Category',
    'File'
)

from datetime import datetime
from typing import Optional, cast

from .base import Base
from sqlalchemy import BigInteger, ForeignKey, func, DateTime, Identity, false
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.core.domain.models.file import File as DFile, FileCategory, SubFileCategory, FileType
from app.core.domain.models.category import Category as DCategory
from app.core.domain.models.user import User as DUser


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f'<User id={self.id!r} created_at={self.created_at!r} deleted_at={self.deleted_at!r}'

    def to_domain(self) -> DUser:
        return DUser(
            self.id,
            self.created_at,
            self.deleted_at,
        )

    @classmethod
    def from_domain(cls, u: DUser) -> 'User':
        return User(
            id=u.id,
            created_at=u.created_at,
            deleted_at=u.deleted_at
        )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user: Mapped[User] = relationship()

    title: Mapped[str]
    description: Mapped[Optional[str]]
    is_favorite: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def to_domain(self) -> DCategory:
        return DCategory(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            description=self.description,
            is_favorite=self.is_favorite,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, c: DCategory) -> 'Category':
        return cls(
            id=c.id,
            user_id=c.user_id,
            title=c.title,
            created_at=c.created_at,
            description=c.description,
            is_favorite=c.is_favorite,
        )


class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    remote_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user: Mapped["User"] = relationship()

    file_type: Mapped[FileCategory]
    sub_type: Mapped[Optional[SubFileCategory]]

    category_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("categories.id"))
    category: Mapped[Optional[Category]] = relationship()

    title: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def to_domain(self, with_category=True) -> DFile:
        file = DFile(
            id=self.id,
            type=FileType(self.file_type, self.sub_type),
            remote_file_id=self.remote_id,
            user_id=self.user_id,
            created_at=self.created_at,
            title=self.title,
        )

        # TODO: improve this code
        if with_category and self.category_id is not None:
            category = cast(Category, self.category)
            file.category = category.to_domain()

        return file
