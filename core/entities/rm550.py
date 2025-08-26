from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from core.database import Base

class RM550(Base):
    __tablename__ = "rm550_config"

    id: Mapped[int] = mapped_column(primary_key=True)
    port: Mapped[str] = mapped_column(String, default='COM3')
    baudrate: Mapped[int] = mapped_column(Integer, default=115200)
    initial_resistance: Mapped[float] = mapped_column(Float, default=100.0)

    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id'))
    project: Mapped["Project"] = relationship( back_populates="rm550")

    def __repr__(self) -> str:
        return f"RM550(id={self.id!r}, port={self.port!r}, baudrate={self.baudrate!r}, initial_resistance={self.initial_resistance!r})"
