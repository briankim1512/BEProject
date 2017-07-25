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
app = Flask(__name__, template_folder='webDir', static_folder='webDir')


@app.route('/')
def main():
    categories = session.query(ItemCat.category, func.count(ItemCat.category))\
                 .group_by(ItemCat.category)
    items = session.query(ItemCat.name, ItemCat.category, ItemCat.id).limit(10)
    return render_template('index.html', categories=categories, items=items)


@app.route('/item/<int:itemId>')
def itemDesc(itemId):
    description = session.query(ItemCat.name, ItemCat.category,\
                  ItemCat.description).filter(ItemCat.id==itemId).first()
    return render_template('itemDesc/index.html', description=description)


@app.route('/categories/<string:catId>')
def catItems(catId):
    items = session.query(ItemCat.name, ItemCat.id).filter(ItemCat.category==catId)
    return render_template('catItems/index.html', items=items, catId=catId)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
