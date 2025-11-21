import os
import datetime
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import random_art_id, get_art, lookup

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///muse.db")


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/art")
def art():

    # Get a random art ID
    art_id = random_art_id()

    # Get the art details from the API
    art = get_art(art_id)
    if art:
        return render_template('art.html', art=art)
    else:
        return render_template("error.html")



@app.route("/history", methods=["GET", "POST"])
def history():
    '''Display a table of previously seen/answered art pieces'''

    history = db.execute("SELECT * FROM history")

    return render_template("history.html", history=history)


@app.route("/reflection", methods=["GET", "POST"])
def reflection():
    '''Display a few questions for the user to reflect on'''

    impressions = request.form.get("impressions")

    db.execute("INSERT INTO history (impressions) VALUES (?), impressions")

    return render_template("reflection.html")


@app.route("/search", methods=["GET","POST"])
def search():
    '''Search by artist, classification or department'''

    # If user submit a request for an artist search
    if request.method == "POST":
        artist = request.form.get('artist')

        # Use API to return a list of ID for artist
        art_ids = lookup(artist)
        arts = []

        # For each ids, get the art details and add to arts list
        if art_ids:
            # LIMITING TO 10 AS A COURTESY FOR API CALLS
            for art_id in art_ids[:10]:
                art_details = get_art(art_id)
                if art_details:
                    arts.append(art_details)

        return render_template("gallery.html", arts=arts)

    return render_template("search.html")
