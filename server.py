# Import SQL related modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, ItemCat
# Import server related modules
from flask import Flask, render_template, abort,\
    url_for, request, redirect
# print("Finished Imports")

# Create a SQL session
engine = create_engine('sqlite:///itemcat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# print("Created an engine")

# Initialization for Flask server
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World'

if __name__ == '__main__':
	app.debug = True
    app.run(host='0.0.0.0', port=8000)
