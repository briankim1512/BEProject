# WARNING--> Execute this code ONLY ONCE, else there will be duplicate entries.
# Imports for the necessary modules to run SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, Item, Category

# Imports to read JSON files
import json

# Make an engine to run SQL sessions and commit entries
engine = create_engine('sqlite:///itemcat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Input data manually into SQL through a JSON file
jsonFile = open("initDBEntries.json", "r")
jsonResult = json.loads(jsonFile.read())
# Input category info first
for i in jsonResult["categories"]:
    catEntry = Category(name=i['name'], id=i['id'])
    session.add(catEntry)
    session.commit()
# Input item info
for i in jsonResult["items"]:
    itemEntry = Item(name=i['name'], description=i['description'],
                     categoryId=i['categoryId'], creator=i['creator'])
    session.add(itemEntry)
    session.commit()
