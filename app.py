from flask import Flask, render_template, request, redirect, flash, session
import csv
import os
import time
from werkzeug.utils import secure_filename
from utils import send_email

# ---------------- APP CONFIG ----------------
app = Flask(__name__)

# Secret key (local & render)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# ---------------- UPLOAD CONFIG ----------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect("/dashboard")
        else:
            flash("Invalid username or password")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/")
    return render_template("dashboard.html")

# ---------------- SEND MAIL ----------------
@app.route("/send", methods=["POST"])
def send():
    if not session.get("admin"):
        return redirect("/")

    csv_file = request.files.get("csv_file")
    message = request.form.get("message")

    if not csv_file or not message:
        flash("CSV file or message missing")
        return redirect("/dashboard")

    filename = secure_filename(csv_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    csv_file.save(file_path)

    sent = 0
    failed = 0

    with open(file_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Support both header names
            email = row.get("Email") or row.get("Email address")

            if email and email.strip():
                success = send_email(email.strip(), message)
                if success:
                    sent += 1
                else:
                    failed += 1

                time.sleep(1)  # Gmail rate-limit safe
            else:
                failed += 1

    flash(f"Emails Sent: {sent} | Failed: {failed}")
    return redirect("/dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
