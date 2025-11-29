import os
import datetime
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_caching import Cache
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import cache, random_art_id, get_art, search_met_api, login_required, fetch_departments, get_department_objects, get_art_from_department


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



@app.route("/")
@login_required
def index():

    # IMPORT APOLOGY PAGES OR CHANGE LOGIC
    return render_template("index.html")



@app.route("/art")
@login_required
def art():

    # Number of attempts for API calls (This is to avoid too many calls at once as per MET's request)
    attempts = 20

    for _ in range(attempts):
        # Get a random art ID
        art_id = random_art_id()

        # Get the art details from the API
        art = get_art(art_id)

        # Render the art
        if art:
            return render_template('art.html', art=art)

    # Render Error page
    return render_template("error.html")



@app.route("/history")
@login_required
def history():
    '''Display a table of previously seen/answered art pieces'''

    user_id = session['user_id']

    history = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)

    return render_template("history.html", history=history)

@app.route("/details")
@login_required
def details():
    '''Display details of an individual record'''

    art_id = request.args.get('art_id')
    art = get_art(art_id)

    return render_template("details.html", art=art)


@app.route("/reflection")
@login_required
def reflection():
    '''Renders a page on which user can reflect. Display art's info'''

    # From art_id value, get art details (cached)
    art_id = request.args.get("art_id")
    art = get_art(art_id)

    return render_template("reflection.html", art=art)



@app.route("/save_reflection", methods=["POST"])
@login_required
def save_reflection():
    '''Save the user's impression on art piece'''

    # Get user ID
    user_id = session['user_id']

    # Get art id and impression from user and form
    art_id = request.form.get("art_id")
    art = get_art(art_id)
    impression = request.form.get("impression")

    # Save to DB
    db.execute("INSERT INTO history (user_id, objectID, objectName, title, artistName, primaryImage, impressions) VALUES (?, ?, ?, ?, ?, ?, ?)", user_id, art["objectID"], art["objectName"], art["title"], art["artistDisplayName"], art["primaryImage"], impression)

    history = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)

    return render_template("history.html", history=history)


@app.route("/search")
@login_required
def search_route():
    '''Search for objects from the collection'''

    query = request.args.get("query")
    dept_id = request.args.get("department_query")

    # Global search
    if query:
        # Use API to return a list of ID for artist
        results = search_met_api(query)
        arts = []

        # For each ids, get the art details and add to arts list
        if results:
            # LIMITING TO 10 AS A COURTESY FOR API CALLS
            for art_id in results[:10]:
                art_details = get_art(art_id)
                if art_details:
                    arts.append(art_details)
                    
        return render_template("gallery.html", arts=arts)

    # Department search
    if dept_id:
        # Use API to return a list of ID for artist
        results = get_department_objects(dept_id)
        arts = []

        # For each ids, get the art details and add to arts list
        if results:
            # LIMITING TO 10 AS A COURTESY FOR API CALLS
            for art_id in results[:10]:
                art_details = get_art_from_department(art_id)
                if art_details:
                    arts.append(art_details)

        return render_template("gallery.html", arts=arts)

    # Default page
    departments = fetch_departments()
    return render_template("search.html", departments=departments)


@app.route("/favorites")
@login_required
def favorites():
    '''Renders a table of the user's favorite paintings'''

    user_id = session['user_id']

    # Get favorites painting from History
    favorites = db.execute("SELECT * FROM history WHERE user_id = ? AND favorite = ?", user_id, '1')

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
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session["user_id"])

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
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
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
@app.route("/like/<int:record_id>", methods=["POST"])
def like(record_id):

    current = db.execute("SELECT favorite FROM history WHERE id = ?", record_id)[0]["favorite"]

    if current == 0:
        db.execute("UPDATE history SET favorite = 1 WHERE id = ?", record_id)
        # Send result for js toggle functionality
        return jsonify({"status": "liked"})

    else:
        db.execute("UPDATE history SET favorite = 0 WHERE id = ?", record_id)
        # Send result for js toggle functionality
        return jsonify({"status": "unliked"})


