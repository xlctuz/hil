from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .channel import Base
from .power_supply import PowerSupply
from .pcie_1762h import Pcie1762h


class ProjectORM(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # many-to-one: a project belongs to one channel
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship("Channel", back_populates="projects")

    power_supply = relationship("PowerSupply", uselist=False, back_populates="project")
    pcie_1762h = relationship("Pcie1762h", uselist=False, back_populates="project")

    def __init__(self, name=""):
        self.name = name


# Domain model classes
class Project:
    def __init__(self, name=""):
        self.id = None
        self.name = name
        self.channel = None  # type: Channel
        self.power_supply = None  # type: PowerSupply
        self.pcie_1762h = None  # type: Pcie1762h


# For backward compatibility
Project = ProjectORM