
import smtplib
import os
from email.mime.text import MIMEText

# ✅ Render / Local ENV variables
EMAIL_ID = os.environ.get("apjcinfotech@gmail.com")
EMAIL_PASS = os.environ.get("lbxcymotamcuhdvj")

def send_email(to_email, message):
    if not EMAIL_ID or not EMAIL_PASS:
        raise Exception("Email credentials not set in environment variables")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ID, EMAIL_PASS)

        msg = MIMEText(message)
        msg["Subject"] = "Meeting Information - Please Read"
        msg["From"] = EMAIL_ID
        msg["To"] = to_email

        server.sendmail(EMAIL_ID, to_email, msg.as_string())
        server.quit()

        return True

    except Exception as e:
        print("ERROR sending mail:", e)
        return False
