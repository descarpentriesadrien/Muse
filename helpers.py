import requests
import random

from flask import session, redirect
from flask_caching import Cache
from functools import wraps

cache = Cache()

def login_required(f): # CS50 Pset recycled
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@cache.cached()
def fetch_object_ids():
    # Filter to return only painting with image (Data is not perfect unfortunately)
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/search?q="painting"&hasImages=true'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()
        return data.get("objectIDs", [])


    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []


def random_art_id():
    '''Fetch a random art object ID from the Met Museum API'''

    # Get id
    ids = fetch_object_ids()

    # Return none if no id was found
    if not ids:
        return None

    # Return a random ID from the list
    return random.choice(ids)


@cache.memoize(timeout=600)
def get_art(art_id):
    '''Get Art details from the MET museum API'''

    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{art_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        art = response.json()

        # If no image in the response, return None
        if art_id is None:
            return None
        if not art.get("primaryImage"):
            return None
        if not art.get("classification") == 'Paintings':
            return None

        # Return Art detail
        return art

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


@cache.cached()
def lookup(artist):
    '''Query for Artist'''
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q={artist}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()
        return data.get("objectIDs", [])


    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

