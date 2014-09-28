import sqlite3
import smtplib
import arrow
from email.mime.text import MIMEText
from email.header import Header
from email_credentials import email_credentials


def send_mail(time_ago, data):
    today = arrow.now().format('dddd, MMM D (YYYY-MM-DD)')
    subject = "It's %s - How did your day go?" % today
    body = "Just reply to this email with your entry.\n\n" \
           "Remember this? %s ago you wrote...\n\n%s" % (time_ago, data)
    mailhost, fromaddr, replytoaddr, toaddrs, credentials = email_credentials()
    username, password = credentials
    msg = MIMEText(body, _charset="UTF-8")
    msg['Subject'] = Header(subject, "utf-8")
    msg['reply-to'] = replytoaddr
    server = smtplib.SMTP(mailhost)
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def get_entry():
    last_year = arrow.now().replace(years=-1).format('YYYY-MM-DD')
    last_month = arrow.now().replace(months=-1).format('YYYY-MM-DD')
    last_week = arrow.now().replace(weeks=-1).format('YYYY-MM-DD')

    day_query = 'select entry from entries where day = ? order by random()'
    random_query = 'select day, entry from entries order by random()'

    with sqlite3.connect('ohlife.db') as db:
        result = db.execute(day_query, (last_year,)).fetchone()
        if result:
            return "One year", result[0]

        result = db.execute(day_query, (last_month,)).fetchone()
        if result:
            return "One month", result[0]

        result = db.execute(day_query, (last_week,)).fetchone()
        if result:
            return "One week", result[0]

        result = db.execute(random_query).fetchone()
        if result:
            num_days_ago = (arrow.now() - arrow.get(result[0])).days - 1
            return "%d days" % num_days_ago, result[1]

    return '', ''


def main():
    data, time_ago = get_entry()
    send_mail(data, time_ago)

if __name__ == '__main__':
    main()
