from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Database connection
engine = create_engine('sqlite:///project.db', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
