from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Database connection
engine = create_engine('sqlite:///project.db', echo=False)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
