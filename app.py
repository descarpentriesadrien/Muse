import os
import datetime
import random
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, get_flashed_messages
from flask_caching import Cache
from flask_paginate import Pagination, get_page_parameter
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import cache, get_painting, search_met_api, login_required, fetch_departments, get_department_objects, get_art, get_user_history, fetch_object_ids, apology


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 600
app.config["DEBUG"] = True

cache.init_app(app)

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///muse.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Number of attempts for API calls (This is to avoid too many calls as per MET's request)
# It is far from efficient, but unfortunately their filtering is not working
API_COURTESY_LIMIT = 25


@app.route("/")
@login_required
def index():

    return render_template("index.html")


@app.route("/art")
@login_required
def random_art():
    '''Random selection of a painting from the MET museum'''

    attempts = 0

    ids = fetch_object_ids()

    # Attempt to get a painting with image URL in response
    while attempts <= API_COURTESY_LIMIT:

        art_id = random.choice(ids)
        art = get_painting(art_id)

        # Render the art
        if art:
            return render_template('art.html', art=art)

        attempts += 1

    # Render Error page
    return apology('Something went wrong, please refresh the page')


@app.route("/history")
@login_required
def history():
    '''Display a table of previously seen/answered art pieces'''

    # Get history for current user
    history = get_user_history(session['user_id'])

    if not history:
        return apology("Something went wrong")

    return render_template("history.html", history=history)


@app.route("/history/<artist_name>")
@login_required
def history_by_artist(artist_name):
    '''Display a table of previously seen/answered art pieces for a specific artis'''

    # artist = request.args.get('artist_name')
    # print(artist)

    # Get history for current user
    history = db.execute("SELECT * FROM history WHERE artistName = ? AND user_id = ?", session['user_id'], artist_name)
    print(history)

    if not history:
        return apology("Something went wrong")

    return render_template("history.html", history=history)


@app.route("/details")
@login_required
def details():
    '''Display details of an individual record (painting only)'''

    art_id = request.args.get('art_id')

    try:
        art_id_int = int(art_id)
    except:
        return apology("This is not a valid art id")

    art = get_painting(art_id)

    if not art:
        return apology("Art not found")

    return render_template("details.html", art=art)


@app.route("/details_dpt")
@login_required
def departments_details():
    '''Display details of an individual record coming from the department search (less constraint)'''

    art_id = request.args.get('art_id')

    try:
        art_id_int = int(art_id)
    except:
        return apology("This is not a valid art id")

    art = get_art(art_id)

    if not art:
        return apology("Art could not be found")

    return render_template("details.html", art=art)


@app.route("/reflection")
@login_required
def reflection():
    '''Renders a page on which user can reflect. Display art's info'''

    # From art_id value, get art details
    art_id = request.args.get("art_id")
    art = get_painting(art_id)

    try:
        art_id_int = int(art_id)
    except:
        return apology("This is not a valid art id")

    if not art:
        return apology("Art could not be found")

    # Get record id
    record_id = request.args.get('id')

    if record_id:
        try:
            record_id_int = int(record_id)
        except:
            return apology("This is not a valid record id")

    # Show the existing data for the field if a record id is found
    if record_id:

        reflections = db.execute(
            "SELECT * FROM history WHERE user_id = ? AND id = ?", session['user_id'], record_id)

        impressions = reflections[0]['impressions']
        connections = reflections[0]['connections']
        meaning = reflections[0]['meaning']
        composition = reflections[0]['composition']

        # Display the form with the existing data if any
        return render_template("reflection.html", art=art, impressions=impressions, connections=connections, meaning=meaning, composition=composition, record_id=record_id)

    return render_template("reflection.html", art=art)


@app.route("/save_reflection", methods=["POST"])
@login_required
def save_reflection():
    '''Save the user's impression on art piece'''

    # Get user ID
    user_id = session['user_id']

    # Get Ids from form
    art_id = request.form.get("art_id")
    record_id = request.form.get('id')

    if art_id:
        try:
            art_id_int = int(art_id)
        except:
            return apology("This is not a valid id")

    # Get Art details
    art = get_painting(art_id)

    if not art:
        return apology("Art could not be found")

    # Get user input
    impressions = request.form.get('impressions')
    connections = request.form.get('connections')
    meaning = request.form.get('meaning')
    composition = request.form.get('composition')

    # Minimum field to input
    if not impressions:
        return apology("Please submit your impressions")

    # Dictionnary to add in DB
    params = {
        'user_id': user_id,
        'objectID': art["objectID"],
        'objectName': art["objectName"],
        'title': art["title"],
        'artistName': art["artistDisplayName"],
        'primaryImage': art["primaryImageSmall"],
        'impressions': impressions,
        'connections': connections,
        'meaning': meaning,
        'composition': composition,
    }

    # If edited, update
    if record_id:
        db.execute("UPDATE history SET impressions = ?, connections = ?, meaning = ?, composition = ? WHERE id = ?",
                   impressions, connections, meaning, composition, record_id)
    # If created, insert
    else:
        db.execute("INSERT INTO history (user_id, objectID, objectName, artistName, title, primaryImage, impressions, connections, meaning, composition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   params['user_id'], params['objectID'], params['objectName'], params['artistName'], params['title'], params['primaryImage'], params['impressions'], params['connections'], params['meaning'], params['composition'])

    return redirect("/history")


@app.route("/delete", methods=["POST"])
@login_required
def delete_reflection():

    # Get Ids
    record_id = request.form.get('id')

    # Validation
    try:
        int_record_id = int(record_id)
    except ValueError:
        return apology("Invalid record ID")

    db.execute("DELETE FROM history WHERE id = ?", int_record_id)

    flash("The reflection was successfully deleted")

    return redirect("/history")


@app.route("/search")
@login_required
def search():
    '''Search for objects from the collection'''

    '''The MET does not always return a painting url in their JSON object.
    In order to avoid displaying multiple results without an image, I then have to
    filter on the back end. This slows down the process drastically and is not
    efficient at all. I currently display only records with a painting (which is the goal of the app).
    I hope this can be taken into consideration'''

    # Pagination set up
    search = False
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 5

    # Slice items for pagination
    start = (page - 1) * per_page
    end = start + per_page

    # Fetch departments
    departments = fetch_departments()
    valid_departments = set()

    # Build a set of valid department id
    for department in departments:
        valid_departments.add(str(department['departmentId']))

    # Get user input
    query = request.args.get("query")
    department_id = request.args.get("department")

    # Validation
    if query is not None and query.strip() == '':
        flash('Please enter a search term or select a department')
        return render_template('search.html', departments=fetch_departments())

    if department_id is not None and not department_id.isdigit():
        return apology('The department ID is an integer.')

    if department_id is not None and department_id not in valid_departments:
        return apology('This department was not found.')

    # Global search
    if query:
        # Use API to return a list of ID for artist
        results = search_met_api(query)
        arts = []

        # For each ids, get the art details and add to arts list (ONLY IF OF TYPE PAINTING AND HAS IMAGE)
        if results:
            # limiting calls as a courtesy
            for art_id in results[:API_COURTESY_LIMIT]:
                art_details = get_painting(art_id)
                if art_details:
                    arts.append(art_details)

        page_arts = arts[start:end]

        pagination = Pagination(page=page, total=len(arts), per_page=per_page, search=False, record_name='arts', css_framework='bootstrap', args=request.args)
        return render_template("gallery.html", arts=page_arts, pagination=pagination, API_COURTESY_LIMIT=API_COURTESY_LIMIT)

    # Department search
    if department_id:

        # Use API to return a list of ID for artist
        results = get_department_objects(department_id)
        arts = []

        # For each ids, get the art details and add to arts list
        if results:
            # Limiting calls as a courtesy
            for art_id in results[:API_COURTESY_LIMIT]:
                art_details = get_art(art_id)
                if art_details:
                    arts.append(art_details)

        page_arts = arts[start:end]

        pagination = Pagination(page=page, total=len(arts), per_page=per_page, search=False, record_name='arts', css_framework='bootstrap', args=request.args)

        return render_template("gallery.html", arts=page_arts, pagination=pagination, API_COURTESY_LIMIT=API_COURTESY_LIMIT)

    # Default page
    return render_template("search.html", departments=departments)


@app.route("/favorites")
@login_required
def favorites():
    '''Renders a table of the user's favorite paintings'''

    user_id = session['user_id']

    # Get favorites painting from History
    favorites = db.execute(
        "SELECT * FROM history WHERE user_id = ? AND favorite = ?", user_id, '1')

    return render_template("favorites.html", favorites=favorites)


@app.route("/register", methods=["GET", "POST"])
def register():  # CS50 Pset recycled
    """Register user"""

    # If the user submit the regitration form
    if request.method == "POST":
        # Get input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validation: ensure username, password and confirmation were provided
        if not username:
            return apology("Please provide a username")

        if not password:
            return apology("Please provide a password")

        if not confirmation:
            return apology("Please confirm the password")

        # Ensure password matches confirmation
        if not password == confirmation:
            return apology("Password and confirmation must match")

        # Insert the new user in the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))
        # Apology if the username already exist
        except ValueError:
            return apology(f"The username '{username}' already exist")

        return redirect("/")

    # Render the form by default
    return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():  # CS50 Pset recycled
    '''Change password'''

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    # Ensure user exists
    if not user:
        return apology("Pleae create an account or login")

    # Username for form, hash for validation
    username = user[0]["username"]
    password = user[0]["hash"]

    # Get input when user submit a password change
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        # Validaton: Ensure input was provided on submission
        if not current_password:
            return apology("Please provide your current password")
        if not new_password:
            return apology("Please provide your new password")
        if not confirm_new_password:
            return apology("Please confirm your new password")

        # Validation: Check for matching passwords
        if not new_password == confirm_new_password:
            return apology("Your new password does not match")
        if not check_password_hash(password, new_password):
            return apology("Incorrect password")

        # Update user's password
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(new_password), session["user_id"])

        # Render a simple page to show success
        return render_template("update.html")

    return render_template("profile.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():  # CS50 Pset recycled
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():  # CS50 Pset recycled
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


'''Like a record and mark it as favorite'''
@login_required
@app.route("/like/<int:record_id>", methods=["POST"])
def like(record_id):

    current = db.execute("SELECT favorite FROM history WHERE id = ?", record_id)[
        0]["favorite"]

    if current == 0:
        db.execute("UPDATE history SET favorite = 1 WHERE id = ?", record_id)
        # Send result for js toggle functionality
        return jsonify({"status": "liked"})

    else:
        db.execute("UPDATE history SET favorite = 0 WHERE id = ?", record_id)
        # Send result for js toggle functionality
        return jsonify({"status": "unliked"})


@login_required
@app.route("/stats")
def stats():
    '''Renders some stats'''

    user_id = session['user_id']

    # Statistics
    favorite_artist_db = db.execute(
        "SELECT artistName, COUNT(*) AS fav_count FROM history WHERE user_id = ? AND favorite = 1 GROUP BY artistName ORDER BY fav_count DESC LIMIT 1", user_id)

    liked_paintings_db = db.execute("SELECT COUNT(*) AS total FROM history WHERE user_id = ? AND favorite = 1", user_id)

    total_reflections_db = db.execute("SELECT COUNT(*) AS total FROM history WHERE user_id = ?", user_id)

    reflected_artist_db = db.execute(
        "SELECT artistName, COUNT(*) AS name FROM history WHERE user_id = ? GROUP BY artistName ORDER BY name DESC LIMIT 1", user_id)

    # Validation
    favorite_artist = favorite_artist_db[0]['artistName'] if favorite_artist_db else None
    liked_paintings = liked_paintings_db[0]['total'] if liked_paintings_db else None
    total_reflections = total_reflections_db[0]['total'] if total_reflections_db else None
    reflected_artist = reflected_artist_db[0]['artistName'] if reflected_artist_db else None


    return render_template("stats.html", favorite_artist=favorite_artist, liked_paintings=liked_paintings, total_reflections=total_reflections, reflected_artist=reflected_artist)
