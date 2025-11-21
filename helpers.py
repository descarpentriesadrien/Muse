import requests
import random

def random_art_id():
    '''Fetch a random art object ID from the Met Museum API'''
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/search?q="painting"&hasImages=true'
    try:
        response = requests.get(url)
        data = response.json()
        object_ids = data.get("objectIDs", [])
        if not object_ids:
            return None
        return random.choice(object_ids)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def get_art(art_id):
    '''Get Art details from the MET museum API'''
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{art_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        art = response.json()
        return {
        "objectID": art["objectID"],
        "objectName": art["objectName"],
        "title": art["title"],
        "artistDisplayName": art["artistDisplayName"],
        "primaryImage": art["primaryImage"],
        "objectDate": art["objectDate"],
        }

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def lookup(artist):
    '''Query for Artist'''
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q={artist}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()
        object_ids = data.get("objectIDs", [])
        if not object_ids:
            return None
        return random.choice(object_ids)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


