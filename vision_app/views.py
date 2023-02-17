from flask import Flask
from flask import render_template
from datetime import datetime
from . import app
from . import webapp

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/checklist/")
def checklist():
    return render_template("checklist.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/calendar/")
def calendar():
    return render_template("calendar.html", events = webapp.events)