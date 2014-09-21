import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email_credentials import email_credentials


def send_mail(data):
    mailhost, fromaddr, toaddrs, subject, credentials = email_credentials()
    username, password = credentials
    subject = 'you are so unbelievably sexy'
    body = 'you sex machine\n\n' + data
    msg = MIMEText(body, _charset="UTF-8")
    msg['Subject'] = Header(subject, "utf-8")
    server = smtplib.SMTP(mailhost)
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def main():
    with sqlite3.connect('db.db') as db:
        print(db.execute('select * from entries').fetchone())

if __name__ == '__main__':
    main()