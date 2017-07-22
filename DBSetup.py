# Initial imports for making a database
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

# Create a table for the database
class ItemCat(Base):
    __tablename__ = 'itemCat'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)

# Create the engine for the database and push data
engine = create_engine('sqlite:///itemcat.db')
Base.metadata.create_all(engine)