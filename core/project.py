from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .channel import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)

    # many-to-one: a project belongs to one channel
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship("Channel", back_populates="projects")

    def __init__(self):
        pass
