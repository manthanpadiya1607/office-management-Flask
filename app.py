from flask import Flask, request,redirect,url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin
from flask_admin import Admin
import sqlite3
from flask import g

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    confirm_password = db.Column(db.String(80))


DATABASE = 'sqlite:///users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/index')
def returnHTML():
    return render_template('index.html')

@app.route('/login')
def returnLogin():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        e = request.form['email']
        p = request.form['password']
        data = SignUp.query.filter_by(email=e, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/signup', methods=['POST','GET'])
def returnSIGNUP():
    if request.method == 'POST':
        try:
            db.session.add(SignUp(first_name=request.form['Your Name'], last_name=request.form['Last Name'], email=request.form['Email address'],password=request.form['Password'],confirm_password=request.form['Confirm Password']))
            db.session.commit()
            return redirect(url_for('/login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('signup.html')






@app.route('/login_validation',methods=['POST'])
def signup_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "the email is {} and password is {}".format(email,password)
if __name__== "__main__":
    app.run(debug=True)


app.run()