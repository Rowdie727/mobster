import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from mobster import app, db, bcrypt, mail, config
from mobster.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from mobster.models import User, Post
from mobster.error_handler import handle_error_404, handle_error_404, handle_error_500
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts, title='Home')

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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_user_img(form_user_img):
    # Hash img file
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_user_img.filename)
    img_filename = random_hex + file_ext
    try:
	images_path = os.path.join('/home/mobadmin/mobster/mobster/static/images', img_filename)
    else:
        images_path = os.path.join(app.root_path, 'static\images', img_filename)
    # Resize img file
    output_size = (125,125)
    new_img = Image.open(form_user_img)
    new_img.thumbnail(output_size)
    new_img.save(images_path)
    return img_filename


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.user_img.data:
            img_file = save_user_img(form.user_img.data)
            current_user.image_file = img_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account info has been updated!', 'danger')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'images/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'danger')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    # Fetch Post(if no post return 404 error)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'danger')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':    
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'danger')
    return redirect(url_for('index'))

@app.route("/user/<string:username>")
def user_pages(username):
    # Display posts by user
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('user_pages.html', posts=posts, title=username, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    sender_address = config.get('MOB_EMAIL')
    message = Message('Password Reset Request', sender=sender_address, recipients=[user.email])
    message.body = f'''To reset your password visit the following link:
    {url_for('reset_token', token=token, _external=True)} '''
    mail.send(message)

@app.route("/reset_password", methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        flash('You must be logged out to request a password reset!', 'danger')
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password, if you do not see an email check your spam folder!', 'danger')
        return redirect(url_for('login'))
    return render_template('request_password_reset.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash('You must be logged out to request a password reset!', 'danger')
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is either invalid or expired!', 'danger')
        return redirect(url_for('request_password_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has successfully been updated!', 'danger')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# Main game routes
@app.route("/attack")
def attack():
    return render_template('game_templates/attack.html', title='ATTACK')

@app.route("/bank")
def bank():
    return render_template('game_templates/bank.html', title='BANK')

@app.route("/equipment")
def equipment():
    return render_template('game_templates/equipment.html', title='EQUIPMENT')
    
@app.route("/godfather")
def godfather():
    return render_template('game_templates/godfather.html', title='GODFATHER')
    
@app.route("/hitlist")
def hitlist():
    return render_template('game_templates/hitlist.html', title='HITLIST')
    
@app.route("/missions")
def missions():
    return render_template('game_templates/missions.html', title='MISSIONS')
    
@app.route("/turf")
def turf():
    return render_template('game_templates/turf.html', title='TURF')
