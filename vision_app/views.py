from flask import Flask, render_template, request, redirect, url_for, jsonify, session,flash
from datetime import datetime
from . import app, webapp
from vision_app import db
from vision_app.models import User

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/checklist/")
def checklist():
    return render_template("checklist.html")

@app.route("/combine/")
def combine():
    return render_template("combine.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route('/register/register-user', methods=['POST'])
def register_user():
    form = request.form
    user = User(
        email = form['email-address'],
        name = form['name']
    )
    user.set_password(form['password'])
    db.session.add(user)   
    db.session.commit()
    return "Successfully registered"

@app.route('/home/login-user', methods=['POST'])
def login_user():
    form = request.form
    user = User.query.filter_by(email = form['email-address']).first()
    if not user:
        flash("Doctor doesn't exist")
        return redirect(url_for('home')) 
    if user.check_password(form['password']):
        session['user'] = user.name 
        return redirect(url_for('calendar')) 
    else:  
        flash('Password was incorrect')
        return redirect(url_for('home')) 

@app.route('/home/logout-user', methods=['POST','GET'])
def logout_user():
    session.pop('user', None)
    return redirect(url_for('home')) 

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/validate-user-registration', methods=['POST'])
def validate_user_registration():
    if request.method == "POST":
        email_address = request.get_json()['email'] 
        user = User.query.filter_by(email=email_address).first()
        if user:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})

@app.route("/calendar/")
def calendar():
    user_name = None
    if session['user']:
        user_name = session['user']
    return render_template("calendar.html", events = webapp.events)