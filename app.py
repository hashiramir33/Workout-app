from flask import Flask, jsonify, request
import pyodbc
from flask_cors import CORS
import os

app= Flask(__name__)
CORS(app)
c= (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:workouttracker2029.database.windows.net,1433;"
    "DATABASE=Workout;"
    "UID=workout;"
    "PWD=Hashir14$$;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
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
    conn = pyodbc.connect(c)
    cur= conn.cursor()
    cur.execute("INSERT INTO Workout (Excer, setsss, Reps, Weight) VALUES (?, ?, ?, ?)",
                data["Excer"],
                data["setsss"],
                data["Reps"],
                data["Weight"]


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


if __name__ == "__main__":
    app.run(debug=True)
