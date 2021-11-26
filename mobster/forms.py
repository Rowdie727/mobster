from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from mobster.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=22)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken, please choose another!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That E-mail is already associated to an account!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=22)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Log in!')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=22)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    user_img = FileField('Update User Image', validators=[FileAllowed(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'bmp', 'heic'])])
    submit = SubmitField('Apply Changes')

    def validate_username(self, username):
        if username.data != current_user.username:  
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken, please choose another!')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That E-mail is already has an associated account!')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that E-Mail!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
    
class BankDepositForm(FlaskForm):
    deposit = IntegerField('Deposit', validators=[NumberRange(min=1)])
    deposit_submit = SubmitField('Deposit')
    
    def validate_deposit(self, deposit):
        try:
            if deposit.data < 0:
                raise ValidationError()
        except:
            pass
   
        
class BankWithdrawForm(FlaskForm):
    withdraw = IntegerField('Withdraw', validators=[NumberRange(min=0)])
    withdraw_submit = SubmitField('Withdraw')
    
    def validate_withdraw(self, withdraw):
        try:
            if withdraw.data < 0:
                raise ValidationError()
        except: 
            pass
        

class EquipmentBuyForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[NumberRange(min=0)])
    buy_submit = SubmitField('Buy')
    sell_submit = SubmitField('Sell')
