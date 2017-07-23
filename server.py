# Import SQL related modules
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, ItemCat
# Import server related modules
from flask import Flask, render_template, abort,\
    url_for, request, redirect

# Create a SQL session
engine = create_engine('sqlite:///itemcat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Initialization for Flask server
app = Flask(__name__, template_folder='pageDir', static_folder='pageDir')


@app.route('/')
def main():
    categories = session.query(ItemCat.category, func.count(ItemCat.category))\
                 .group_by(ItemCat.category)
    return render_template('home.html', categories=categories)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
