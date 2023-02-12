from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from app.forms import SignUpForm, LoginForm, ContactForm
from app.models import User
#from app.api import RNA_dict, FRET_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/julia')
def julia():
    return render_template('julia.html')

@app.route('/contact', methods=["GET","POST"])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(f"Name:{form.name.data}, E-mail:{form.email.data}, Subject:{form.subject.data}, Message:{form.message.data}")
            flash(f'Thank you, {form.name.data}. We will get back to you as soon as possible.','success')
            return redirect(url_for('index'))
        else:
            return render_template('contact.html', form=form)
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/papers')
def papers():
    return render_template('papers.html', RNA_dict=RNA_dict, FRET_dict=FRET_dict)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        if check_user:
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))