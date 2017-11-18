from db.database_connection import session
from db.database import User, Category, Item
from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
from flask import session as login_session
from sqlalchemy import desc
import json
from oauthHandler import exchange_authorization_code, verify_credentials
from oauthHandler import get_user_info, revoke_token
from pixabay_connector import findItemPicture
from flask import make_response
import random
import string

app = Flask(__name__)


# ------------------------
# MAIN PAGE
# ------------------------


@app.route('/')
@app.route('/catalog')
def mainPage():
    """
    Function to generate the main page with the list of all categories
    The html is rendered with all categories on the DB and the Latest
    items
    """
    # Fetch all categories from the database
    categories = session.query(Category).all()
    # Fetch the latest items from the DB
    items = session.query(Item).order_by(
                                desc(Item.id)).limit(len(categories)).all()
    # Check if the User is autorized
    if 'username' not in login_session:
        # User is not authorized render the public catalog template
        return render_template(
                            'publiccatalog.html',
                            categories=categories,
                            items=items)
    # User is authorized render the private catalog template
    return render_template('catalog.html', categories=categories, items=items)


# ------------------------
# ITEM CRUD OPERATIONS
# ------------------------


# CREATE
###########################


@app.route('/catalog/new', methods=['GET', 'POST'])
def addItem():
    """
    Function to add a new item to the database
    """
    authorized = True
    # Check if the user is authorized
    if 'username' not in login_session:
        authorized = False

    # Check if the request method is a POST
    if request.method == 'POST':
        # Perform a CSRF state check
        if request.args.get('state') != login_session['state']:
            return redirectWithFlash('mainPage')

        # Fetch a single category from the database based on the category name
        category = session.query(Category).filter_by(
                        name=request.form['category_name']).first()

        if authorized:
            # Create an item based on the information received from the client
            item = Item(name=request.form['name'],
                        description=request.form['description'],
                        user_id=login_session['user_id'],
                        picture=findItemPicture(request.form['name']),
                        category_id=category.id)
            # Persist the item
            addToDB(item)
            # Return a flash message
            flash("Successfully added item: %s" % item.name)
            # Redirect to the category's catalog
            return redirect(url_for('showCatalog',
                            category_name=category.name))
        else:
            # If the user is not authorized redirect to the login page
            return redirectWithFlash('showLogin')
    else:
        # Request is a GET request
        if not authorized:
            # User is not authorized, redirect to the login page
            return redirectWithFlash('showLogin')

        # Fetch all categories from the database
        categories = session.query(Category).all()
        # Generate a state token for CSRF Protection
        state = generateState()
        # Render the template
        return render_template(
                                'additem.html',
                                categories=categories,
                                STATE=state)

# READ
###########################


@app.route('/catalog/<string:category_name>/items')
def showCatalog(category_name):
    """
    Function to show all of the items of a givem category
    """
    category_name = category_name.replace("+", " ")

    # Fetch all categories from the database
    categories = session.query(Category).all()
    # Fetch a single category from the database based on the category name
    category = session.query(Category).filter_by(name=category_name).one()
    # Fetch all of the items in the category
    items = session.query(Item).filter_by(category_id=category.id).all()
    # Check if the user is authorized
    if 'username' not in login_session:
        # User is not authorized render the public template
        return render_template(
                                'publiccategory.html',
                                items=items,
                                chosencategory=category,
                                categories=categories,
                                item_count=len(items))
    # User is authorized render the private template
    return render_template(
                            'category.html',
                            items=items,
                            chosencategory=category,
                            categories=categories,
                            item_count=len(items))


@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
    """
    Function to show a specific category item based on the category name
    and the item name
    """

    # Fetch a single category based on the category name
    category = session.query(Category).filter_by(
                            name=category_name.replace("+", " ")).first()
    # Fetch a single item based on the item name
    item = session.query(Item).filter_by(
                                name=item_name.replace("+", " ")).first()
    # Check if the user is authorized
    if ('username' not in login_session
            or item.user_id != login_session['user_id']):
        # User is not authorized render the public template
        return render_template('publicviewitem.html', item=item)
    # User is authorized render the private template
    return render_template('viewitem.html', item=item)

# UPDATE
###########################


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    """
    Function to update a specific item on the DB based on the item name
    """
    # Parse the item name for DB access
    item_name = item_name.replace("+", " ")
    authorized = True
    # Fetch a single item based on the item name
    item = session.query(Item).filter_by(name=item_name).first()
    # Check if the user is authorized
    if ('username' not in login_session
            or login_session['user_id'] != item.user_id):
        authorized = False
    # Check if the request method is a POST
    if request.method == 'POST':
        # Perform a CSRF state check
        if request.args.get('state') != login_session['state']:
            return redirectWithFlash('mainPage')
        # Fetch a single category based on the category name
        category = session.query(Category).filter_by(
                                    name=request.form['category_name']).first()
        if authorized:
            # Perform the relevant Updates

            if request.form['name']:
                item.name = request.form['name']
                # Fetch the item's picture from the Pixabay API
                item.picture = findItemPicture(item.name)

            # Associate the item to the category
            item.category_id = category.id
            if request.form['description']:
                item.description = request.form['description']
            # Persist the Item
            addToDB(item)
            # Redirect to the items category page
            flash("Item: %s updated successfuly" % item.name)
            return redirect(url_for('showCatalog',
                                    category_name=category.name))
        else:
            # User is unauthorized redirect to the login page
            return redirectWithFlash('showLogin')
    else:
        if not authorized:
            return redirectWithFlash('showLogin')
        # Fetch all categories from the database
        categories = session.query(Category).all()
        # Generate CSRF Token
        state = generateState()
        # Render the template
        return render_template(
                                'edititem.html',
                                item=item,
                                categories=categories, state=STATE)

# DELETE
###########################


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    """
    Function to delete a specific item from the database
    """
    # Parse the item name for DB access
    item_name = item_name.replace("+", " ")
    authorized = True
    # Fetch a single item based on the item name
    item = session.query(Item).filter_by(name=item_name).first()
    if ('username' not in login_session
            or login_session['user_id'] != item.user_id):
        authorized = False
    # Check if the request method is a POST
    if request.method == 'POST':
        # Check if the user is authorized
        if authorized:
            # Delete the item from the database
            session.delete(item)
            session.commit()
            # Send a flash message and redirect to the main page
            flash("Item %s deleted successfully" % item.name)
            return redirect(url_for('mainPage'))
    else:
        # Check if the user is authorized
        if authorized:
            # User is authorized render the template
            return render_template('deleteitem.html', item=item)
        # User is not authorized redirect to the login page
        return redirectWithFlash('showLogin')


# ------------------------
# AUTHENTICATION / AUTHORIZATION
# ------------------------


# OAUTH VALIDATION FUNCTION
###########################

@app.route('/oauth/<string:provider>', methods=['POST'])
def oauthLogin(provider):
    """
    Function to authenticate and authorize a user's login session by exchanging
    information with an OAUTHv2 provider
    """
    if provider == 'google':
        # Check the CSRF Token
        if request.args.get('state') != login_session['state']:
            return engineer_response(
                                'Invalid state parameter.', 401)
        code = request.data
        # Exchange the one time code for an access token
        flow_response = exchange_authorization_code(code)
        # Check if the request was successful
        if flow_response[0] is False:
            # If the request was not successful send a negative resp code
            return engineer_response(
                    'Failed to upgrade the authorization code.', 401)
        credentials = flow_response[1]
        # Check if the user's access token is valid
        verified_credentials = verify_credentials(credentials)
        if verified_credentials[0] is False:
            # The user's token is invalid send negative response
            return engineer_response(verified_credentials[2],
                                     verified_credentials[1])

        # Save the session's credentials(If existent) in a variable
        stored_access_token = login_session.get('access_token')
        stored_gplus_id = login_session.get('gplus_id')
        gplus_id = credentials.id_token['sub']

        # Check if the current user is already logged in
        if stored_access_token is not None and gplus_id == stored_gplus_id:
            return engineer_response(
                                'Current user is already connected.', 200)

        # Save the access credentials in the session
        login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id

        # Get the user info from OAUTHv2 provider
        data = get_user_info(credentials)

        # Save the user info in the session
        populate_user_session_info(data)

        # Get the user ID from the DB
        user_id = getUserID(login_session['email'])
        if user_id is None:
            # Create the user if the user does not exist
            user_id = createUser(login_session)
        # Add the user id to the session
        login_session['user_id'] = user_id
        flash("You are now logged in as %s" % login_session['username'])
        return render_template('loginresult.html', user=data)


# LOGIN PAGE GENERATOR
###########################

@app.route('/login')
def showLogin():
    """
    The showLogin function is responsible for rendering the login page
    with a state token for CSRF Protection
    """
    # Generating a state token for CSRF Protection
    state = generateState()
    return render_template('login.html', STATE=state)


# LOGOUT FUNCTION
###########################


@app.route('/logout')
def logout():
    """
    The logout method is used to delete the user's session in the oauth
    provider and to redirect the user to the main page
    """

    # Only disconnect a connected user.
    if login_session['access_token'] is None:
        return engineer_response('Current user not connected.', 401)

    status = revoke_token(login_session)
    if status == '200':
        # Reset the user's sesson.
        delete_session()
        # Redirect the user to the login page once the user has been logged out
        flash("You have logged out with no errors")
        return redirect(url_for('mainPage'))
    else:
        # For whatever reason, the given token was invalid.
        if 'username' in login_session:
            delete_session()
        flash("You have logged out with errors")
        return redirect(url_for('mainPage'))

# ------------------------
# JSON PRESENTERS
# ------------------------

# JSON ENDPOINT FUNCTIONS
###########################


@app.route('/catalog/JSON')
def categoriesJSON():
    """
    Function to provide the catalog information in JSON Format
    Information is serialized and passed back to the client
    """
    # Fetch all categories from the database
    categories = session.query(Category).all()
    # Fetch the latest items from the DB
    items = session.query(Item).order_by(
                                desc(Item.id)).limit(len(categories)).all()
    return jsonify(Categoies=[c.serialize for c in categories],
                   Items=[i.serialize for i in items])


@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def showItemJSON(category_name, item_name):
    """
    Function to return the item and category information in JSON Format
    Information is serialized and passed back to the client
    """

    # Fetch a single category based on the category name
    category = session.query(Category).filter_by(
                            name=category_name.replace("+", " ")).first()
    # Fetch a single item based on the item name
    item = session.query(Item).filter_by(
                                name=item_name.replace("+", " ")).first()
    return jsonify(Category=category.serialize,
                   Item=item.serialize)


@app.route('/catalog/<string:category_name>/items/JSON')
def showCatalogJSON(category_name):
    """
    Function to show all of the items of a givem category
    """
    category_name = category_name.replace("+", " ")

    # Fetch all categories from the database
    categories = session.query(Category).all()
    # Fetch a single category from the database based on the category name
    category = session.query(Category).filter_by(name=category_name).one()
    # Fetch all of the items in the category
    items = session.query(Item).filter_by(category_id=category.id).all()

    return jsonify(Categories=[c.serialize for c in categories],
                   Category=category.serialize,
                   Items=[i.serialize for i in items])


# ------------------------
# HELPER FUNCTIONS
# ------------------------


# JSON RESPONSE GENERATOR
###########################

def engineer_response(text, code):
    """
    Function to generate a JSON response
    """
    response = make_response(json.dumps(text), code)
    response.headers['Content-Type'] = 'application/json'
    return response


# DB OBJECT PERSISTER FUNCTION
##############################

def addToDB(obj):
    """
    Function to persist an object(obj) to the database
    """
    session.add(obj)
    session.commit()


# USER CREATION FUNCTION
###########################

def createUser(login_session):
    """
    Function to create a user based on the information stored on the session
    object, the information is collected from the OAUTHv2 provider
    """
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# FLASHING FUNCTION
###########################

def redirectWithFlash(page):
    """
    Function to redirect a user to a specific page with a flash message
    The page which will be redirected to cannot contain route parameters
    """
    flash("You are not authorized to perform the action you want to perform")
    return redirect(url_for(page))


# USER ID FETCHING FUNCTION
###########################


def getUserID(email):
    """
    Function to get a user's Id based on a user's email (The email is stored on
    the database or on the user's session object)
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# SESSION RESET FUNCTION
###########################


def delete_session():
    """
    Function to delete a user's login session upon logout
    """
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['user_id']
    del login_session['email']
    del login_session['picture']


# LOGIN PAGE GENERATOR
###########################

def populate_user_session_info(data):
    """
    Function to populate a user's session based on data collected from the
    OAUTHv2 provider
    """
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


# CSRF TOKEN GENERATOR FUNCTION
###########################


def generateState():
    """
    Function to generate a CSRF State protection token to protect against CSRF
    Attacks
    """
    # Generate CSRF State string token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return state


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
