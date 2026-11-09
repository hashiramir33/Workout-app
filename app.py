from flask import Flask, jsonify, request,redirect,session
import pyodbc
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

import os
load_dotenv()
app= Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}}, supports_credentials=True)
app.secret_key = os.getenv("Secret")
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True
)



c= (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tcp:workouttracker2029.database.windows.net,1433;"
    "DATABASE=Workout;"
    "UID=workout;"
    "PWD=Hashir14$$;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

oauth = OAuth(app)

oauth.register(
    name="google",
    client_id=os.getenv("Gcd"),
    client_secret=os.getenv("Gcs"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)





@app.route("/")
def home():
    return "Workouut Tracker server is running"

@app.route("/workouts", methods=["GET"])
def workouts():
    conn = pyodbc.connect(c)
    cur= conn.cursor()
    cur.execute("SELECT * FROM Workout")
    rows= cur.fetchall()
    return jsonify([
        {
            "id": row[0],
            "Excer": row[1],
            "setsss": row[2],
            "Reps": row[3],
            "Weight": row[4]

        }
        for row in rows
    ])





@app.route("/workouts", methods=["POST"])
def addw():
    data = request.get_json()

    exc = data["Excer"]
    setsss = float(data["setsss"])
    rep = float(data["Reps"])
    weight = float(data["Weight"])

    if exc =="" or len(exc)>50:
        return jsonify({"error": "name isnt valid"}), 400

    if setsss <= 0 or rep <= 0 or weight <= 0:
        return jsonify({"error": "must be a positive number"}), 400









    conn = pyodbc.connect(c)
    cur= conn.cursor()
    cur.execute("INSERT INTO Workout (Excer, setsss, Reps, Weight) VALUES (?, ?, ?, ?)",
                exc,
                setsss,
                rep,
                weight
                


    )

    conn.commit()
    return jsonify({"message": "Workout Added"})


@app.route("/workouts", methods=["DELETE"])
def clear():
    conn = pyodbc.connect(c)
    cur= conn.cursor()


    cur.execute("DELETE FROM Workout")
    conn.commit()

    return jsonify({"message" : "cleared"})


@app.route("/auth/login")
def login():
   
    ru = os.getenv("Gurl")
    


    return oauth.google.authorize_redirect(ru)





@app.route("/auth/callback")
def auth_callback():
    token = oauth.google.authorize_access_token()

    user = token.get("userinfo")

    if not user:
        return "no inffo", 400

    session["user"] = {
        "id": user["sub"],
        "name": user.get("name"),
        "email": user.get("email")
    }

    return redirect("http://localhost:5500/Main.html")


@app.route("/api/user")
def current_user():
    user = session.get("user")

    if not user:
        return jsonify({"logged_in": False}), 401

    return jsonify({
        "logged_in": True,
        "name": user["name"],
        "email": user["email"]
    })


@app.route("/auth/logout")
def logout():
    session.clear()
    return redirect("/")





if __name__ == "__main__":
    app.run(debug=True)

