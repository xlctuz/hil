from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.database import Base
from typing import List, Optional


class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True)
    index: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)

    # 一个Channel可以有多个Project（一对多）
    projects: Mapped[List["Project"]] = relationship(back_populates="channel", foreign_keys='Project.channel_id')

    current_project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("project.id"))
    current_project = relationship("Project", foreign_keys=[current_project_id])

    def __repr__(self) -> str:
        return f"Channel(id={self.id!r}, name={self.name!r}"
