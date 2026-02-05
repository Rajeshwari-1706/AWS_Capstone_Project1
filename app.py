# Note: Database operations and user authentication are simplified for demonstration purposes.
# In a production environment, ensure to implement proper security measures.
from flask import Flask, render_template, request, redirect, session
import sqlite3
import boto3
import uuid
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = "train_secret_key"

# AWS Config
REGION = "us-east-1"
dynamodb = boto3.resource("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)

# Tables
users_table = dynamodb.Table("Users")
trains_table = dynamodb.Table("Trains")
bookings_table = dynamodb.Table("Bookings")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:148761664676:project_topics"

def send_notification(subject, message):
    try:
        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject, Message=message)
    except ClientError as e:
        print("SNS Error:", e)

def get_db():
    conn = sqlite3.connect("train.db")
    conn.row_factory = sqlite3.Row
    return conn
app = Flask(__name__)
app.secret_key = "train_secret"
@app.route("/")
def home():
    return redirect("/login")   
# ✅ SIGNUP (only once)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # You can save user to DB here
        return redirect("/login")
    return render_template("signup.html")
# ✅ LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["email"]
        return redirect("/search")
    return render_template("login.html")
# ✅ SEARCH
@app.route("/search", methods=["GET", "POST"])
def search():
    trains = []
    if request.method == "POST":
        trains = [
            (1, "Express 101", "Chennai", "Bangalore", "10:00 AM"),
            (2, "Superfast 202", "Delhi", "Mumbai", "6:00 PM")
        ]
    return render_template("search.html", trains=trains)
# ✅ BOOKING (only once)
@app.route("/booking/<int:train_id>")
def booking(train_id):
    return render_template("booking.html", train_id=train_id)
# ✅ PAYMENT
@app.route("/payment", methods=["POST"])
def payment():
    return render_template(
        "payment.html",
        train_id=request.form["train_id"],
        name=request.form["name"],
        age=request.form["age"]
    )
# ✅ TICKET
@app.route("/ticket", methods=["POST"])
def ticket():
    return render_template(
        "ticket.html",
        name=request.form["name"],
        age=request.form["age"],
        train_id=request.form["train_id"]
    )
# ✅ DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])
# ✅ LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
if __name__ == "__main__":
    app.run(debug=True)# Note: Database operations and user authentication are simplified for demonstration purposes.
# In a production environment, ensure to implement proper security measures.            


