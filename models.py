from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)

    password = db.Column(db.String(255))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float)

    location = db.Column(db.String(100))

    risk_score = db.Column(db.Integer)

    status = db.Column(db.String(50))