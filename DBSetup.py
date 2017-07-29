# Initial imports for making a database
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


# Create a table for categories
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


# Create a table for items related to the categories
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    categoryId = Column(Integer, ForeignKey('category.id'))
    description = Column(String)
    creator = Column(String)

# Create the engine for the database and push data
engine = create_engine('sqlite:///itemcat.db')
Base.metadata.create_all(engine)
