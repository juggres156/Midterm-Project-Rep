from typing import ValuesView
from flask import Flask, render_template, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json, os
import sqlite3 as sql
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration_database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.String(50), primary_key=True)
    user_firstName = db.Column(db.String(50))
    user_lastName = db.Column(db.String(50))
    user_Email = db.Column(db.String(50))
    user_username = db.Column(db.String(50))
    user_password = db.Column(db.String(50))

    def __init__(self, user_id, user_firstName, user_lastName, user_Email, user_username, user_password):
        self.user_id = user_id
        self.user_firstName = user_firstName
        self.user_lastName = user_lastName
        self.user_Email = user_Email
        self.user_username = user_username
        self.user_password = user_password
        

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "user_firstName" , "user_lastName", "user_Email", "user_username", "user_password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/home")
@app.route("/")
def home():
    return render_template("devops.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form["uname"]
        password = request.form["password"]

        stmt = text("SELECT * FROM User where user_username=:username and user_password=:password")
        stmt = stmt.columns(User.user_id, User.user_firstName, User.user_lastName, User.user_Email, User.user_username, User.user_password)
        
        users = db.session.query(User).from_statement(stmt).params(username=username, password=password).all()
        user = users_schema.dump(users)
        #print(result)
        #customer_schema.jsonify(result)
        
        if (user is None):
            user = None
            return render_template("login.html")
        else:
            if(len(user)>0):
                if (user[0]['user_username'] == username and user[0]['user_password'] == password):
                    return render_template("success.html") 
                else:
                    return render_template("login.html")

    return render_template ("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        userId = datetime.now().strftime("%d%H%M%S")
        fname = request.form ['fname']
        lname = request.form ['lname']
        username = request.form ['username']
        Email = request.form ['Email']
        password = request.form ['password']

        new_customer = User(userId, fname, lname, Email, username, password)
        db.session.add(new_customer)
        db.session.commit()

        msg="Successfully Register"
        
        return render_template("result.html", msg=msg)


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)