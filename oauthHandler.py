from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# ------------------------
# OAUTH HANDLER SCRIPT
# ------------------------

"""
This is the OAUTHv2 handler script that handles communication with google's
oauth provider
"""

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


def exchange_authorization_code(code):
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # Exchange the code with the oauth provider
        credentials = oauth_flow.step2_exchange(code)
        return (True, credentials)
    except FlowExchangeError:
        return (False, )


def verify_credentials(credentials):
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return (False, 500, result.get('500'))

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return (False, 401, "Token's user ID doesn't match given user ID.")

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return (False, 401, "Token's client ID does not match app's.")
    return (True,)


def get_user_info(credentials):
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    return answer.json()


def revoke_token(login_session):
    access_token = login_session.get('access_token')

    # Revoke an access token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    return result['status']
