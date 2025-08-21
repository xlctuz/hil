from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChannelORM(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    name = Column(String)

    # one-to-many: a channel has many projects
    projects = relationship("ProjectORM", back_populates="channel")

    def __init__(self, index, name=""):
        self.index = index
        self.name = name


# Domain model class
class Channel:
    def __init__(self, index, name=""):
        self.index = index
        self.name = name


# For backward compatibility
Channel = ChannelORM