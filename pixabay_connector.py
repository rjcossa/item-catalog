import requests
import httplib2
import json
import sys
import codecs

# ------------------------
# PIXABAY CONNECTOR SCRIPT
# ------------------------

"""
This is the Pixabay API connector script which retrieves images from Pixabay
and returns a URL
"""

PIXABAY_API_KEY = ""


def findItemPicture(queryString):
    queryString = queryString.replace(" ", "+")
    # Add the query string and the API Key to the URL
    url = (
          "https://pixabay.com/api/?key=%s&q=%s&image_type=photo&pretty=true" %
          (PIXABAY_API_KEY, queryString)
           )
    h = httplib2.Http()
    # Get information from server
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    # Return the picture's URL
    return result['hits'][0]['webformatURL']
