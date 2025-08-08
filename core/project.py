from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .channel import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # many-to-one: a project belongs to one channel
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship("Channel", back_populates="projects")

    power_supply = relationship("Power_supply_it6302", uselist=False, back_populates="project")
    pcie_1762h = relationship("Pcie_1762h", uselist=False, back_populates="project")

    def __init__(self, name=""):
        self.name = name
