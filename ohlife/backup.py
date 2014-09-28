import smtplib
import sqlite3
import arrow
import gzip
from io import StringIO
from pandas.io.sql import read_sql
from email_credentials import email_credentials
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64


def send_mail(subject, body, attachment=None):
    mailhost, fromaddr, replytoaddr, toaddrs, credentials = email_credentials()
    username, password = credentials
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject)
    msg.attach(MIMEText(body))
    if attachment is not None:
        payload, filename = attachment
        part = MIMEBase('application', "octet-stream")
        part.set_payload(payload)
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
        msg.attach(part)
    server = smtplib.SMTP(mailhost)
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def get_attachment():
    with sqlite3.connect('ohlife.db') as db:
        df = read_sql('select * from entries', db)
    with StringIO() as tmp_file:
        df.to_csv(tmp_file, index=False)
        tmp_file.seek(0)
        csv = tmp_file.read().encode('utf-8')
    compressed_csv = gzip.compress(csv)
    filename = 'ohlife_%s.csv.gz' % arrow.now().format('YYYYMMDD')
    return compressed_csv, filename


def main():
    subject = 'ohlife entries as of %s' % arrow.now().format('YYYYMMDD')
    body = 'See attachment'
    send_mail(subject, body, get_attachment())

if __name__ == '__main__':
    main()