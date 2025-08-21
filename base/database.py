from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('sqlite:///project.db', echo=False)
Session = sessionmaker(bind=engine)
