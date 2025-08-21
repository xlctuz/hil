from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .channel import Base


class Status(Enum):
    HIGH = "high"
    LOW = "low"
    NA = "na"


class Pcie1762hDiChannel:
    def __init__(self, index):
        self.index = index
        self.name = ""


class Pcie1762hDoChannel:
    def __init__(self, index):
        self.index = index
        self.name = ""
        self.status = Status.NA


class Pcie1762hDiChannelORM(Base):
    __tablename__ = 'pcie_1762h_di_channel'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)

    pcie_1762h_id = Column(Integer, ForeignKey('pcie_1762h.id'))
    pcie_1762h = relationship("Pcie1762hORM", back_populates="di_channels")


class Pcie1762hDoChannelORM(Base):
    __tablename__ = 'pcie_1762h_do_channel'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)
    status = Column(SQLEnum(Status), default=Status.NA)

    pcie_1762h_id = Column(Integer, ForeignKey('pcie_1762h.id'))
    pcie_1762h = relationship("Pcie1762hORM", back_populates="do_channels")


class Pcie1762hORM(Base):
    __tablename__ = 'pcie_1762h'
    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("ProjectORM", back_populates="pcie_1762h", uselist=False)
    do_channels = relationship("Pcie1762hDoChannelORM", back_populates="pcie_1762h", cascade="all, delete-orphan")
    di_channels = relationship("Pcie1762hDiChannelORM", back_populates="pcie_1762h", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        # Initialize domain model attributes
        if not self.do_channels:
            self.do_channels = [Pcie1762hDoChannelORM(index=i) for i in range(16)]
        if not self.di_channels:
            self.di_channels = [Pcie1762hDiChannelORM(index=i) for i in range(16)]
        super().__init__(**kwargs)


# For backward compatibility, we can create an alias
Pcie1762h = Pcie1762hORM
Pcie1762hDiChannel = Pcie1762hDiChannelORM
Pcie1762hDoChannel = Pcie1762hDoChannelORM