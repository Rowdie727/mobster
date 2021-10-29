from flask import render_template, url_for, flash, redirect, request
from mobster import app, db, bcrypt
from mobster.forms import RegistrationForm, LoginForm
from mobster.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

test_posts = [
    {
        'user': 'Test User1',
        'title': 'Test Title1', 
        'msg_body': 'Test Blog Body1 Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti, error! Optio doloremque nisi quae excepturi perferendis, soluta officiis mollitia a!',
        'date_posted': 'Jan 1, 2021'
    },
    {
        'user': 'Test User2',
        'title': 'Test Title2', 
        'msg_body': 'Test Blog Body2 Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti, error! Optio doloremque nisi quae excepturi perferendis, soluta officiis mollitia a!',
        'date_posted': 'Jan 2, 2021'
    }
]

@app.route("/")
def index():
    return render_template('index.html', test_posts=test_posts, title='Home')

@app.route("/login", methods=['GET', 'POST'])
def login():
    # If logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # Validate login
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('You have been logged in', 'danger')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful, please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    # If logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash user password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create user object
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        # Add user to Db
        db.session.add(user)
        # Commit changes to Db
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'danger')
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')