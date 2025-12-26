from flask import Flask, render_template, request, redirect, flash
import csv, os, time
from utils import send_email

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            return redirect("/dashboard")
        else:
            flash("Invalid Login")
    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------- SEND MAIL ----------------
@app.route("/send", methods=["POST"])
def send():
    csv_file = request.files["csv_file"]
    message = request.form["message"]

    if not csv_file or not message:
        flash("CSV or Message missing")
        return redirect("/dashboard")

    file_path = os.path.join(UPLOAD_FOLDER, csv_file.filename)
    csv_file.save(file_path)

    sent = 0
    failed = 0

    with open(file_path, newline='', encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        print("CSV Headers:", reader.fieldnames)

        for row in reader:
            email = (
                row.get("Email address")
                or row.get("Email")
            )

            print("Row:", row)

            if email and email.strip():
                ok = send_email(email.strip(), message)
                if ok:
                    sent += 1
                else:
                    failed += 1
                time.sleep(1)   # Gmail rate limit safe
            else:
                print("Email missing in row")

    flash(f"Sent: {sent} | Failed: {failed}")
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
