import os
import secrets
from datetime import datetime
from flask import url_for
from flask_mail import Message
from mobster import app, on_server, config, mail
from mobster.models import User
from PIL import Image

def pay_users():
    for user in User.query.all():
        if user.stats.user_total_income > 0:
            print(f'{user.id}//{datetime.utcnow()}: {user.username} paid {user.stats.user_total_income}!')
            user.cash_on_hand += user.stats.user_total_income


def save_user_img(form_user_img):
    # Hash img file
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_user_img.filename)
    img_filename = random_hex + file_ext
    # Check which image path to use
    if on_server:
        images_path = os.path.join('/home/mobadmin/mobster/mobster/static/images', img_filename)
    else:
        images_path = os.path.join(app.root_path, 'static/images', img_filename)
    # Resize img file
    output_size = (125,125)
    new_img = Image.open(form_user_img)
    new_img.thumbnail(output_size)
    new_img.save(images_path)
    return img_filename

def send_reset_email(user):
    token = user.get_reset_token()
    sender_address = config.get('MOB_EMAIL')
    message = Message('Password Reset Request', sender=sender_address, recipients=[user.email])
    message.body = f'''To reset your password visit the following link:
    {url_for('reset_token', token=token, _external=True)} '''
    mail.send(message)