# https://www.youtube.com/watch?v=B1IsCbXp0uE
import smtplib
from email.message import EmailMessage


def send_alert(subject, body, to):
    msgs = [EmailMessage(), EmailMessage(), EmailMessage()]
    user = "cashparking2022@gmail.com"
    for msg in msgs:
        msg.set_content(body)
        msg['subject'] = subject
        msg['from'] = user
    msgs[0]['to'] = to + "@txt.att.net"
    msgs[1]['to'] = to + "tmomail.net"
    msgs[2]['to'] = to + "vtext.com"
    
    password = "tbrlzeerppbxamrz"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    for msg in msgs:
        try:
            server.send_message(msg)
        except:
            pass
    server.quit()

if __name__ == "__main__":
    send_alert("hi", "stf", "3193839547")