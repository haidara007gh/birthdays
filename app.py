import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure sqlite3 Library to use SQLite database
conn = sqlite3.connect("birthdays.db", check_same_thread = False)
cur = conn.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        
        # Validate and remember
        if name and month and day:
            info = (name, month, day)
            cur.execute("INSERT INTO birthdays (name, month, day) VALUES(?,?,?)",info)
            conn.commit()   
        return redirect("/")
    else:
        # Display the entries in the database on index.html
        rows = cur.execute("SELECT * FROM birthdays").fetchall()
        return render_template("index.html", rows = rows)

@app.route("/delete", methods = ["POST"])
def delete():
    id = (request.form.get("id"),)
    if id:
        cur.execute("DELETE FROM birthdays WHERE id = ?",id)
        conn.commit()
    return redirect("/")
