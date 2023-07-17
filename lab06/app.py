from flask import Flask, render_template, request, redirect, url_for
import re
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "passwords.db"

# Database setup
def initialize_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# Password format checker
def check_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not password[-1].isdigit():
        return False
    return True

# Routes
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/report", methods=["POST"])
def report():
    username = request.form.get("username")
    password = request.form.get("password")

    if check_password(password):
        initialize_database()
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO passwords VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        result = "Password meets the requirements and has been stored in the database."
    else:
        result = "Password does not meet the requirements."

    return render_template("report.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
