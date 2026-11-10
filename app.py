from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from models import db,User,Transaction
from fraud_engine import calculate_risk

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///database.db'

app.config['SECRET_KEY'] = "fraud_secret"

db.init_app(app)

bcrypt = Bcrypt(app)

CORS(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():

    return {
        "message":"Real Time Fraud Detection API Running"
    }

@app.route("/register",methods=["POST"])
def register():

    data=request.json

    hashed=bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user=User(
        name=data["name"],
        email=data["email"],
        password=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message":"user registered"
    })

@app.route("/login",methods=["POST"])
def login():

    data=request.json

    user=User.query.filter_by(
        email=data["email"]
    ).first()

    if user and bcrypt.check_password_hash(
        user.password,
        data["password"]
    ):
        return {
            "message":"success"
        }

    return {
        "message":"invalid credentials"
    },401

@app.route("/transaction",methods=["POST"])
def transaction():

    data=request.json

    risk,status = calculate_risk(
        data["amount"],
        data["location"]
    )

    trans=Transaction(

        amount=data["amount"],
        location=data["location"],
        risk_score=risk,
        status=status
    )

    db.session.add(trans)
    db.session.commit()

    return jsonify({

        "risk_score":risk,
        "status":status

    })

if __name__ == "__main__":
    app.run(debug=True)