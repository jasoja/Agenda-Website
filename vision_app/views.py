from flask import Flask, render_template, request, redirect, url_for, jsonify, session,flash
from datetime import datetime
from . import app, webapp
from vision_app import db
from vision_app.models import User, Item

@app.route("/")
def home():
    if 'user' in session.keys():
        return redirect(url_for("checklist"))
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/about2/")
def about2():
    return render_template("aboutLoggedIn.html")

@app.route("/classes/")
def classes():
    user_id = None
    if session['user']:
        user_id = session['user']
        return render_template("classes.html")
    return render_template("classes.html")

@app.route("/checklist/", methods = ['POST', 'GET'])
def checklist():
    user_id = None
    if session['user']:
        user_id = session['user']
        tasks = Item.query.filter_by(user_id=user_id)
        return render_template('checklist.html', tasks=tasks)
    return render_template('checklist.html')

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
    flash("Successfully registered, please login.")
    return redirect(url_for('home'))

@app.route('/validate-user-registration', methods=['POST'])
def validate_user_registration():
    if request.method == "POST":
        email_address = request.get_json()['email'] 
        user = User.query.filter_by(email=email_address).first()
        if user:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})
        
@app.route('/home/login-user', methods=['POST'])
def login_user():
    form = request.form
    user = User.query.filter_by(email = form['email-address']).first()
    if not user:
        flash("User doesn't exist")
        return redirect(url_for('home')) 
    if user.check_password(form['password']):
        session['user'] = user.id 
        return redirect(url_for('calendar')) 
    else:  
        flash('Password was incorrect')
        return redirect(url_for('home')) 

@app.route('/home/logout-user', methods=['POST','GET'])
def logout_user():
    session.pop('user', None)
    return redirect(url_for('home')) 


@app.route("/checklist/add_task", methods=['POST'])
def add_task():
    form = request.form
    taskItem = Item.query.filter_by(task=form['task_name']).first()
    if not taskItem:
        taskItem = Item(
            task = form['task_name'],
            course_category=form['course_category'],
            course_weight=form['course_weight'],
            date= datetime.strptime(form['due_date'], '%m/%d/%y %H:%M:%S'),
            user_id = session['user']
        )

        db.session.add(taskItem)
        db.session.commit()
        flash('Task successfully added to check list')
        return redirect(url_for('checklist'))

    else:
        flash('Task already exists')
        return redirect(url_for('checklist'))

@app.route("/calendar/")
def calendar():
    user_id = None
    if session['user']:
        user_id = session['user']
        tasks = Item.query.filter_by(user_id=user_id)
        return render_template('calendar.html', events = webapp.events ) 
    return render_template("calendar.html", events = webapp.events)

