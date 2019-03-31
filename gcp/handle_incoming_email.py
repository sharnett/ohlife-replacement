import datetime
import logging
import re

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import ndb

import webapp2


class DailyEntry(ndb.Model):
    date = ndb.DateProperty()
    entry = ndb.StringProperty()


def _extract_plaintext(mail_message):
    bodies = mail_message.bodies('text/plain')
    content_type, payload = list(bodies)[0]
    body = payload.decode()
    pattern = r'(.*)On.*com> wrote:\s+>'
    m = re.search(pattern, body, re.DOTALL)
    if not m:
        return body
    return m.group(1).strip()


def _extract_date(subject):
    pattern = r'(\d\d\d\d-\d\d-\d\d)'
    m = re.search(pattern, subject)
    if m is not None:
        return m.group(1)
    raise ValueError("Couldn't extract date from %s" % subject)


def _write_to_db(date_string, entry):
    if date_string is None or entry is None:
        raise ValueError("Failed to record %s, %s; one of them is missing." % (date_string, entry))
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    if DailyEntry.query(DailyEntry.date==date).get():
        raise ValueError("Entry for %s already exists" % date_string)
    daily_entry = DailyEntry(
        date=date,
        entry=entry)
    daily_entry.put()


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        subject = mail_message.subject
        logging.info("subject: " + subject)
        date_string = _extract_date(subject)
        logging.info("day: " + date_string)
        entry = _extract_plaintext(mail_message)
        logging.info("entry[:10]: " + entry[:10])
        _write_to_db(date_string, entry)
        logging.info("wrote to db")


# [START app]
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
# [END app]