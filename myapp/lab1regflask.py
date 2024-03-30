from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import Error

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1226@localhost3306/cyberproject'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
@app.route('/')
def lab1reg():
    return render_template('lab1reg.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        flash('Login successful!')
        return redirect(url_for('lab1reg'))
    else:
        flash('Invalid email or password')
        return redirect(url_for('lab1login'))
@app.route('/')
def index():
    return render_template('lab1reg.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return 'Passwords do not match', 400

    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('user created successfully')
        return redirect(url_for('lab1reg'))
    except Error as e:
        return f'There was a problem registering the user: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)