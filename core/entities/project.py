from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.database import Base
from typing import List


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
    channel: Mapped["Channel"] = relationship(back_populates="projects", foreign_keys=[channel_id])

    power_supply: Mapped["PowerSupply"] = relationship(back_populates="project")
    pcie_1762h: Mapped["Pcie1762h"] = relationship(back_populates="project")

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, name={self.name!r}"
