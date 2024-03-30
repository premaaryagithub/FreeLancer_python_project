import os
from flask import Flask, render_template, request, redirect, url_for,flash,jsonify,render_template_string
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import Error
from werkzeug.exceptions import HTTPException
from flask_mail import Mail,Message
from datetime import timedelta
import re
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1226@localhost:3306/cyberproject1'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = '003'
db = SQLAlchemy(app)
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.iiitkottayam.ac.in'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dulla22bcy59@iiitkottayam.ac.in'
app.config['MAIL_PASSWORD'] = 'qpvz kgib hykw hqas'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email is None:
            raise BadRequestKeyError('email')
        password = request.form.get('password')
        if password is None:
            raise BadRequestKeyError('password')

        user1 = User1.query.filter_by(email=email).first()

        if user1 and user1.password == password:
            first_letter = email[0].upper()
            name = user1.username
            email_ = email
            flash('Login successful!')
            return redirect(url_for('lab1', first_letter=first_letter,name=name,email_=email_))

        else:
            flash('Invalid email or password')
    elif request.method == "GET":
          email = None
          password = None
    if User1.query.count() == 0:
        flash('You must register first to access this page.')
        return render_template('lab1reg.html')

    return render_template('lab1login.html', email=email, password=password)
@app.route('/logout')
def logout():
    return render_template("lab1login.html")    
@app.route('/lab1/<first_letter>/<name>/<email_>')
def lab1(first_letter,name,email_):
    return render_template('lab1.html', first_letter=first_letter,name=name,email_=email_)

class User1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
class BadRequestKeyError(HTTPException):
     def __init__(self, message=None):
        HTTPException.__init__(self, 'Bad Request: The browser (or proxy) sent a request that this server could not understand.', response=message)

     def get_response(self, environ=None):
        if environ is not None:
            status = '400 Bad Request'
        else:
            status = ' Bad Request'
        response = self.make_subclass_response(status)
        if self.response is not None:
            response.make_conditional(request.if_modified_since)
            response.data = to_bytes(str(self.response))
            response.content_type = self.content_type
            if self.headers:
                response.headers.extend(self.headers)
        return response
@app.errorhandler(BadRequestKeyError)
def handle_bad_request_key_error(error):
    return error.get_response(), error.code        

@app.route('/')
def lab1reg():
    next_url = request.args.get('next')
    return render_template('lab1reg.html', next=next_url)
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            return 'Please enter your email address.', 400
        user1 = User1.query.filter_by(email=email).first()
        if not user1:
            return 'User not registered previously. Please register first.', 404
        otp = generate_otp()
        send_otp(email, otp)
        session['otp'] = otp
        session['forgot_password_email'] = email
        session.permanent = True
        return 'OTP has been sent to your email address. Please enter it to reset your password.', 200
    return render_template('forgot_password.html')
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    otp = request.args.get('otp')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    if not otp:
        return 'Please enter OTP.', 400
    if new_password != confirm_password:
        return 'Passwords do not match.', 400
    if session['otp'] != otp:
        return 'Invalid OTP.', 401
    user1 = User1.query.filter_by(email=session['forgot_password_email']).first()
    user1.password = generate_password_hash(new_password)
    db.session.commit()
    return 'Password has been reset successfully.', 200
def generate_otp():
    return ''.join(random.choice('0123456789') for _ in range(6))
def send_otp(email, otp):
    html_content = render_template('email_otp.html', otp=otp)

    msg = Message(
        subject='OTP for Password Reset',
        recipients=[email],
        html=html_content
    )
    mail.send(msg)

def generate_password_hash(password):
    return pbkdf2_sha256.hash(password.encode())
def check_password_hash(password, hashed_password):
    return pbkdf2_sha256.verify(password.encode(), hashed_password)    
@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return 'Passwords do not match', 400
    if not re.fullmatch(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
        return 'Password must be at least 8 characters long, contain at least one special character, one digit, and no spaces', 400
    if User1.query.filter_by(email=email).first():
        return "Email is already registered. Please enter another email or log in."
    if User1.query.filter_by(username=username).first():
        return "Username is already taken. Please enter another username or log in."

    try:
        new_user = User1(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        first_letter = email[0].upper()
        name = username
        email_ = email
        flash('user created successfully')
        return redirect(url_for('lab1', first_letter=first_letter,name=name,email_=email_))
    except Error as e:
        return f'There was a problem registering the user: {e}', 500
if __name__ == '__main__':
    app.run(debug=True)