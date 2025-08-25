from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Pci1720uChannel(Base):
    __tablename__ = 'pci1720u_channel'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    name = Column(String)
    voltage = Column(Float)

    pci1720u_id = Column(Integer, ForeignKey('pci1720u.id'))
    pci1720u = relationship("Pci1720u", back_populates="channels")


class Pci1720u(Base):
    __tablename__ = 'pci1720u'

    id = Column(Integer, primary_key=True)
    device_number = Column(Integer, default=0)

    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship("Project", back_populates="pci1720u", uselist=False)

    channels = relationship("Pci1720uChannel", back_populates="pci1720u", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if not self.channels:
            # The PCI-1720U has 4 AO channels
            self.channels = [Pci1720uChannel(index=i) for i in range(4)]
        super().__init__(**kwargs)
