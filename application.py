import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    transactions = db.execute("SELECT symbol, sum(shares) AS shares FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                              user_id=session["user_id"])

    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                           user_id=session["user_id"])

    rows = []
    total_sum = 0

    for ta in transactions:
        symbol = ta["symbol"]
        shares = ta["shares"]

        quote = lookup(symbol)

        price = quote.get("price")
        total = shares * price

        total_sum += total

        if shares is not 0:
            row = generate_row(symbol, shares, price, total)
            rows.append(row)

    cash = generate_row("CASH", None, None, user_cash[0]["cash"])
    rows.append(cash)

    total_sum += user_cash[0]["cash"]

    total_sum = '${:,.2f}'.format(total_sum)

    return render_template("index.html", rows=rows, total_sum=total_sum)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Add cash to your balance"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        try:
            cash = int(request.form.get("cash"))

        except ValueError:
            return apology("please enter an integer", 400)

        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :user_id",
                   cash=cash, user_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cash.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))

        # Ensure symbol is provided
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol exists
        if not quote:
            return apology("symbol does not exist", 400)

        try:
            share_count = int(request.form.get("shares"))

        except ValueError:
            return apology("please enter an integer", 400)

        # Ensure share_count is a positive integer
        if share_count < 0:
            return apology("cannot buy negative amount of shares", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        if rows[0]["cash"] < quote["price"] * share_count:
            return apology("you do not have enough money", 400)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=quote["symbol"], shares=int(request.form.get("shares")), price=quote["price"])

        db.execute("UPDATE users SET cash = cash - :shares * :price WHERE id = :user_id",
                   shares=int(request.form.get("shares")), price=quote["price"], user_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = :user_id",
                              user_id=session["user_id"])

    rows = []

    for ta in transactions:
        symbol = ta["symbol"]
        shares = ta["shares"]
        price = ta["price"]
        transacted = ta["transacted"]

        if shares is not 0:
            row = generate_history_row(symbol, shares, price, transacted)
            rows.append(row)

    return render_template("history.html", rows=rows)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was provided
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        quote = lookup(request.form.get("symbol"))

        # Ensure symbol exists
        if not quote:
            return apology("symbol does not exist", 400)

        price = "${:,.2f}".format(quote.get("price"))

        # Redirect user to home page
        return render_template("quoted.html", symbol=quote.get("symbol"), price=price)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))

        shares = db.execute("SELECT sum(shares) AS shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol",
                            user_id=session["user_id"], symbol=request.form.get("symbol"))

        # Ensure symbol was submitted
        if not quote:
            return apology("symbol does not exist", 400)

        # Ensure the user owns shares of the stock
        if shares[0]["shares"] < 1:
            return apology("you do not own any shares of this stock", 400)

        try:
            share_count = int(request.form.get("shares"))

        except ValueError:
            return apology("please enter an integer", 400)

        # Ensure share_count is a positive integer
        if share_count < 0:
            return apology("cannot sell negative amount of shares", 400)

        # Ensure the user owns enough shares of the stock
        if shares[0]["shares"] < int(request.form.get("shares")):
            return apology("you do not own enough shares of this stock", 400)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares * -1, :price)",
                   user_id=session["user_id"], symbol=quote["symbol"], shares=int(request.form.get("shares")), price=quote["price"])

        db.execute("UPDATE users SET cash = cash + :shares * :price WHERE id = :user_id",
                   shares=int(request.form.get("shares")), price=quote["price"], user_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        symbols = db.execute("SELECT symbol, sum(shares) AS shares FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                             user_id=session["user_id"])
        for symbol in symbols:
            if symbol["shares"] <= 0:
                symbols.remove(symbol)

        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


def generate_row(symbol, shares, price, total):
    row = {
        "symbol": symbol,
        "shares": shares if shares is not None else "",
        "price": "${:,.2f}".format(price) if price is not None else "",
        "total": "${:,.2f}".format(total),
    }

    return row


def generate_history_row(symbol, shares, price, transacted):
    row = {
        "symbol": symbol,
        "shares": shares if shares is not None else "",
        "price": "${:,.2f}".format(price) if price is not None else "",
        "transacted": transacted,
    }

    return row


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)