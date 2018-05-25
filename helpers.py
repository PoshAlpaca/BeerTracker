import csv
import os
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def generate_row(result):

    row = {
            "date": result.get("date"),
            "amount": abs(result.get("amount")),
    }

    if result.get("amount") > 0:
        row["from"] = "You"
        row["to"] = result.get("friend")

    elif result.get("amount") < 0:
        row["from"] = result.get("friend")
        row["to"] = "You"

    else:
        row["from"] = ""
        row["to"] = ""

    return row


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function