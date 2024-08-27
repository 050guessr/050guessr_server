import keys
import smtplib, ssl
from email.mime.text import MIMEText



def send_mail(receiver_email, tijdelijk_wachtwoord):
    sender_email = "050guessr@gmail.com"
    password = keys.gmail_password

    message = MIMEText("""\
Hi,
ik heb een tijdelijk wachtwoord ingesteld. wijzig je wachtwoord hierna.
tijdelijk wachtwoord: {tijdelijk_wachtwoord}""".format(tijdelijk_wachtwoord=tijdelijk_wachtwoord))
    message["Subject"] = "reset wachtwoord"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())