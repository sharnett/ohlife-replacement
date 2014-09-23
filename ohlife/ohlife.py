import sqlite3
import smtplib
import arrow
from email.mime.text import MIMEText
from email.header import Header
from email_credentials import email_credentials


def send_mail(data):
    today = arrow.now().format('dddd, MMM D (YYYY-MM-DD)')
    subject = "It's %s - How did your day go?" % today
    body = "Forward this email to the secret address with your entry.\n\n" \
           "Remember this? One year ago you wrote...\n" + data
    mailhost, fromaddr, toaddrs, credentials = email_credentials()
    username, password = credentials
    msg = MIMEText(body, _charset="UTF-8")
    msg['Subject'] = Header(subject, "utf-8")
    server = smtplib.SMTP(mailhost)
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def get_last_year_entry():
    last_year = arrow.now().replace(years=-1).format('YYYY-MM-DD')
    with sqlite3.connect('db.db') as db:
        query = 'select entry from entries where day = ?'
        return db.execute(query, (last_year,)).fetchone()[0]


def main():
    data = get_last_year_entry()
    send_mail(data)


if __name__ == '__main__':
    main()

