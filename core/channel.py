from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)

    # one-to-many: a channel has many projects
    projects = relationship("Project", back_populates="channel")

    def __init__(self, index):
        self.index = index
