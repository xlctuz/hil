from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .channel import Base
from .power_supply import PowerSupply
from .pcie_1762h import Pcie1762h


class Project(Base):
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
