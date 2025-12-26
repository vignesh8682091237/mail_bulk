import smtplib
from email.mime.text import MIMEText

EMAIL_ID = "apjcinfotech@gmail.com"
EMAIL_PASS = "lbxcymotamcuhdvj"   # new app password podunga

def send_email(to_email, message):
    try:
        print("Connecting SMTP...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("Logging in...")
        server.login(EMAIL_ID, EMAIL_PASS)

        msg = MIMEText(message)
        msg["Subject"] = "Meeting Information - Please Read"
        msg["From"] = EMAIL_ID
        msg["To"] = to_email

        server.sendmail(EMAIL_ID, to_email, msg.as_string())
        server.quit()

        print("Mail sent to:", to_email)
        return True

    except Exception as e:
        print("ERROR sending to:", to_email)
        print(e)
        return False
