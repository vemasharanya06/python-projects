from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def create_database():
    connection = sqlite3.connect("database.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/request", methods=["GET", "POST"])
def request_page():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        category = request.form["category"]
        description = request.form["description"]

        connection = sqlite3.connect("database.db")

        connection.execute("""
            INSERT INTO requests
            (name, roll, category, description, status)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll, category, description, "Pending"))

        connection.commit()
        connection.close()

        return "Request submitted successfully!"

    return render_template("request.html")


@app.route("/requests")
def view_requests():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    requests = connection.execute(
        "SELECT * FROM requests"
    ).fetchall()

    connection.close()

    return render_template("requests.html", requests=requests)


create_database()


if __name__ == "__main__":
    app.run(debug=True)