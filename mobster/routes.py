from flask import render_template, url_for, flash, redirect
from mobster import app
from mobster.forms import RegistrationForm, LoginForm
from mobster.models import User, Post

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
    return render_template('index.html', test_posts=test_posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    dummy_admin = 'admin'
    dummy_pw = '1234'
    if form.validate_on_submit():
        if form.username.data == dummy_admin and form.password.data == dummy_pw:
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

