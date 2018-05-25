import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, generate_row, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///beer.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # User reached page via POST
    if request.method == "POST":

        if not request.form.get("friend"):
            return apology("must provide friend name", 400)

        elif not request.form.get("amount"):
            return apology("must provide amount", 400)

        elif not request.form.get("action"):
            return apology("must choose an action", 400)

        try:
            amount = int(request.form.get("amount"))

        except ValueError:
            return apology("please enter an integer", 400)

        if request.form.get("action") == "get":
            amount *= -1

        # Insert new transaction into database
        db.execute("INSERT INTO transactions (user_id, friend, amount) VALUES (:user_id, :friend, :amount)",
                   user_id=session["user_id"], friend=request.form.get("friend"), amount=amount)

        return redirect("/compare/{}".format(request.form.get("friend")))

    # User reached page via GET
    else:

        # Get username of current user
        results = db.execute("SELECT username FROM users WHERE id = :user_id",
                             user_id=session["user_id"])
        username = results[0].get("username")

        # Get balance of current user
        results = db.execute("SELECT sum(amount) AS total FROM transactions WHERE user_id = :user_id",
                             user_id=session["user_id"])
        balance = results[0].get("total")

        # Get friends of current user
        results = db.execute("SELECT friend FROM transactions WHERE user_id = :user_id GROUP BY friend",
                             user_id=session["user_id"])

        # Unpack friend names into a simple array
        friends = []
        for result in results:
            friend = result.get("friend")
            friends.append(friend)

        # Get transaction history of current user
        results = db.execute("SELECT date, amount, friend FROM transactions WHERE user_id = :user_id ORDER BY date DESC",
                             user_id=session["user_id"])

        # Unpack data to make it more accessible to Jinja template
        rows = []
        for result in results:
            row = generate_row(result)
            rows.append(row)

        return render_template("index.html", username=username, balance=balance if balance is not None else 0, friends=friends, rows=rows)


@app.route("/compare")
@app.route("/compare/<friend>")
@login_required
def compare(friend=None):

    # Get list of the current user's transactions
    results = db.execute("SELECT date, amount, friend FROM transactions WHERE user_id = :user_id AND friend = :friend ORDER BY date""",
                         user_id=session["user_id"], friend=friend)

    rows = []
    for result in results:
        row = generate_row(result)
        rows.append(row)

    # Get score of current user and of their friend
    results = db.execute("SELECT abs(sum(amount)) AS total, CASE WHEN amount > 0 THEN 'user' WHEN amount < 0 THEN 'friend' ELSE 'other' END AS person FROM transactions WHERE user_id = :user_id AND friend = :friend GROUP BY person",
                         user_id=session["user_id"], friend=friend)

    score = {}
    for result in results:
        if result.get("person") == "user":
            score["user"] = result.get("total")

        elif result.get("person") == "friend":
            score["friend"] = result.get("total")

        else:
            score["other"] = result.get("total")

    if "user" not in score:
        score["user"] = 0

    if "friend" not in score:
        score["friend"] = 0

    difference = score["user"] - score["friend"]

    return render_template("compare.html", friend=friend, score=score, difference=difference, rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username is not being used yet
        elif len(rows) != 0:
            return apology("username already exists", 400)

        # Ensure password and confirmation were submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"),
                   hash=generate_password_hash(request.form.get("password")))

        # Query database for username again
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)