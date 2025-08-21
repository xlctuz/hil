from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .channel import Base


class Status(Enum):
    HIGH = "high"
    LOW = "low"
    NA = "na"


class Pcie1762hDiChannel(Base):
    __tablename__ = 'pcie_1762h_di_channel'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)

    pcie_1762h_id = Column(Integer, ForeignKey('pcie_1762h.id'))
    pcie_1762h = relationship("Pcie1762h", back_populates="di_channels")


class Pcie1762hDoChannel(Base):
    __tablename__ = 'pcie_1762h_do_channel'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)
    status = Column(SQLEnum(Status), default=Status.NA)

    pcie_1762h_id = Column(Integer, ForeignKey('pcie_1762h.id'))
    pcie_1762h = relationship("Pcie1762h", back_populates="do_channels")


class Pcie1762h(Base):
    __tablename__ = 'pcie_1762h'
    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="pcie_1762h", uselist=False)
    do_channels = relationship("Pcie1762hDoChannel", back_populates="pcie_1762h", cascade="all, delete-orphan")
    di_channels = relationship("Pcie1762hDiChannel", back_populates="pcie_1762h", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        # Initialize domain model attributes
        if not self.do_channels:
            self.do_channels = [Pcie1762hDoChannel(index=i) for i in range(16)]
        if not self.di_channels:
            self.di_channels = [Pcie1762hDiChannel(index=i) for i in range(16)]
        super().__init__(**kwargs)

