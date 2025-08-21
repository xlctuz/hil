from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base.database import Base
from .power_supply import PowerSupply
from .pcie_1762h import Pcie1762h


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    channel_index = Column(Integer)

    power_supply = relationship("PowerSupply", uselist=False, back_populates="project")
    pcie_1762h = relationship("Pcie1762h", uselist=False, back_populates="project")

    def __init__(self, name=""):
        self.name = name
