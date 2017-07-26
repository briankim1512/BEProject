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


# 'Home page' of the website that returns the categories and most recent items
@app.route('/')
def main():
    categories = session.query(ItemCat.category, func.count(ItemCat.category))\
                 .group_by(ItemCat.category)
    items = session.query(ItemCat.name, ItemCat.category, ItemCat.id)\
        .order_by(ItemCat.id.desc()).limit(10)
    return render_template('index.html', categories=categories, items=items)


# The page that allows the registered user to create a new item
@app.route('/newItem', methods=['GET', 'POST'])
def newItem():
    if request.method == 'GET':
        categories = session.query(ItemCat.category).group_by(ItemCat.category)
        return render_template('newItem/index.html', categories=categories)
    if request.method == 'POST':
        item = ItemCat(name=request.form['name'],
                       category=request.form['category'],
                       description=request.form['description'])
        session.add(item)
        session.commit()
        return redirect(url_for('main'))


# The page that returns the items of the desired category
@app.route('/categories/<string:catId>')
def catItems(catId):
    # Hard-coded the "All Items" category since it doesn't exist in the DB
    if catId == "All Items":
        items = session.query(ItemCat.name, ItemCat.id)
    # This is for the categories that the link provides
    else:
        items = session.query(ItemCat.name, ItemCat.id)\
                .filter(ItemCat.category == catId)
    categories = session.query(ItemCat.category, func.count(ItemCat.category))\
        .group_by(ItemCat.category)
    return render_template('catItems/index.html', items=items, catId=catId,
                           categories=categories)


# The page that returns the item category and description
@app.route('/item/<int:itemId>')
def itemDesc(itemId):
    description = session.query(ItemCat.name, ItemCat.category,
                                ItemCat.description)\
                                .filter(ItemCat.id == itemId).first()
    # Makes sure that there is data from the itemId provided
    if description is None:
        abort(404)
    return render_template('itemDesc/index.html', description=description,
                           itemId=itemId)


# This page allows the user to edit or delete the selected item
@app.route('/item/<int:itemId>/<string:mod>', methods=['GET', 'POST'])
def modItem(itemId, mod):
    if request.method == 'GET':
        # Creates a form from the itemId provided
        if mod == 'edit':
            description = session.query(ItemCat.name, ItemCat.category,
                                        ItemCat.description)\
                                        .filter(ItemCat.id == itemId).first()
            categories = session.query(ItemCat.category,
                                       func.count(ItemCat.category))\
                                .group_by(ItemCat.category)
            return render_template('itemDesc/editItem/index.html',
                                   itemId=itemId,
                                   description=description,
                                   categories=categories)
        # Makes sure that the user wants to delete the item
        elif mod == 'delete':
            return render_template('itemDesc/delItem/index.html',
                                   itemId=itemId)
        else:
            abort(404)
    if request.method == 'POST':
        # Edits sql entry based on the form provided
        if mod == 'edit':
            item = session.query(ItemCat).filter(ItemCat.id == itemId).first()
            item.name = request.form['name']
            item.category = request.form['category']
            item.description = request.form['description']
            session.commit()
            return redirect(url_for('itemDesc', itemId=itemId))
        # Deletes the sql entry from the link provided
        elif mod == 'delete':
            item = session.query(ItemCat).filter(ItemCat.id == itemId).first()
            session.delete(item)
            session.commit()
            return redirect(url_for('main'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
