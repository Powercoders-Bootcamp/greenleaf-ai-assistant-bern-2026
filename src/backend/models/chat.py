from __future__ import annotations

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    anonymous_user_key: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
        nullable=False,
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
    )
