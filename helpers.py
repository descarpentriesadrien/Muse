import requests
import random

from cs50 import SQL
from flask import session, redirect, render_template
from flask_caching import Cache
from functools import wraps

cache = Cache()

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///muse.db")

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

def apology(message, code=400): #CS50 PSET recycled
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


'''Fetch list of avaialable objects in collection'''
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

'''Get Art details from the MET museum API'''
@cache.memoize(timeout=60 * 60 * 24)
def get_painting(art_id):

    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{art_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        art = response.json()

        # If missing info in the response (image, classification), return None
        if art_id is None:
            return None
        if not art.get("primaryImage"):
            return None
        if not art.get("classification") == 'Paintings':
            return None

        # Return Art object
        return art

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


'''Query for art pieces from the API'''
@cache.memoize(timeout=60 * 60 * 24)
def search_met_api(query):
    '''Query for Global search'''
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()
        return data.get("objectIDs", [])


    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


'''Get the list of the MET departments'''
@cache.cached()
def fetch_departments():
    # Filter to return only painting with image (Data is not perfect unfortunately)
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()
        return data.get("departments", [])


    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []


'''Get a list of objects from the selected MET department'''
@cache.memoize(timeout=60 * 60 * 24)
def get_department_objects(dept_id):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    params = {"departmentIds": dept_id}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("objectIDs", [])
    except Exception as e:
        print(f"Error fetching department objects: {e}")
        return []


'''Get art from department, with or without constraint due to unclean data'''
@cache.memoize(timeout=60 * 60 * 24)
def get_art(art_id):
    '''Get Art details from the MET museum API'''

    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{art_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        art = response.json()

        # If missing info in the response (image, classification), return None
        if art_id is None:
            return None

        # Return Art detail
        return art

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def get_user_history(user_id):

    # Get history for current user
    try:
        return db.execute("SELECT * FROM history WHERE user_id = ?", user_id)
    except Exception as e:
        return []
