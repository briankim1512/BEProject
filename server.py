# Import SQL related modules
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from DBSetup import Base, ItemCat
# Import server related modules
from flask import Flask, render_template, abort,\
    url_for, request, redirect, jsonify
from flask import session as login_session

# Import Auth related modules
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Declare client ID for Google Oauth2.0
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

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


# This route provides the JSON file for others to use
@app.route('/catalog.json')
def jsonCat():
    results = session.query(ItemCat)
    items = {}
    for i in results:
        items.update({i.name: {}})
        item = {"id": i.id, "category": i.category,
                "description": i.description}
        items[i.name].update(item)
    return jsonify(items)


# This route provides the login page for the user
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login/index.html', STATE=state)


# This route provides the callback from the google auth
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.header['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match"),
                401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    output = ''
    output += login_session['username']

    return output

if __name__ == '__main__':
    app.secret_key = "OIHFG4HOP398HFLKJ43HT2498"
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
