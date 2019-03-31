import datetime
import os
import sys

import arrow
from google.cloud import datastore
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

FROM_EMAIL = 'from@fake.com'
TO_EMAIL = 'to@fake.com'

def _get_entry():
    client = datastore.Client('ohlife')
    today = arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    last_year = today.replace(years=-1).datetime
    last_month = today.replace(months=-1).datetime
    last_week = today.replace(weeks=-1).datetime

    query = client.query(kind='DailyEntry')
    query.add_filter('date', '=', last_year)
    result = list(query.fetch(1))
    if result:
        return "One year", result[0]['entry']

    query = client.query(kind='DailyEntry')
    query.add_filter('date', '=', last_month)
    result = list(query.fetch(1))
    if result:
        return "One month", result[0]['entry']

    query = client.query(kind='DailyEntry')
    query.add_filter('date', '=', last_week)
    result = list(query.fetch(1))
    if result:
        return "One week", result[0]['entry']

    return '', ''

# [START functions_ohlife_pubsub]
def ohlife_pubsub(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    apikey = os.environ.get('SENDGRID_API_KEY')
    if apikey is None:
    	return 'api key not set'
    sg = sendgrid.SendGridAPIClient(apikey=apikey)

    from_email = Email(FROM_EMAIL)
    to_email = Email(TO_EMAIL)
    today = arrow.now().format('dddd, MMM D (YYYY-MM-DD)')
    subject = 'It\'s %s - How did your day go?' % today
    time_ago, entry = _get_entry()
    body = 'Just reply to this email with your entry.\n\n' \
           'Remember this? %s ago you wrote...\n\n%s' % (time_ago, entry)
    content = Content('text/plain', body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return str(response.body)
# [END functions_ohlife_pubsub]
