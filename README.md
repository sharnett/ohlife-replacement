ohlife-replacement
==================

ohlife was an email-based diary thing that shut down in October 2014. This aims
to do basically the same thing.

I've used two different methods to deploy it:

1. A cheap VPS from lowendbox.com
2. Google Cloud Platform (free tier)

# Cheap VPS method

You need an email address for this. I'm using gmail.

Create a file called email_credentials.py that looks like this:

```python
def email_credentials():
    mailhost = "smtp.gmail.com"
    fromaddr = "XXX@gmail.com"
    replytoaddr = "OhLife <XXX@cloudmailin.net>"
    toaddrs = ["YYY"]
    credentials = ("XXX", "ZZZ")
    return mailhost, fromaddr, replytoaddr, toaddrs, credentials
```

Run the import.py script with your ohlife.txt export file:

```
python import.py ohlife_export.txt
```

Set up a web server to run listen.py. I'm just using the flask development
server inside a tmux session. I found a virtual private server for less than
$1/month from [lowendbox](https://lowendbox.com/).

Sign up for a free account at [cloudmailin](https://www.cloudmailin.com/) or
equivalent. Basically you want something that converts email to an http post.
Send the http post to the webserver in the previous step.

Set up a daily cron job to run ohlife.py.

When ohlife.py sends you an email, reply to the cloudmailin email address.


# Google Cloud Platform

You'll probably want to install the GCP developer tools and Sendgrid python stuff to test locally.

1. Create a new Datastore (optionally with some seed data) with kind = 'DailyEntry' and two columns:
    1. 'Date' of type Date and time
    1. 'Entry' of type String
1. Set up a free Sendgrid account and note your API key.
1. Deploy the email handler script.
    1. Edit the 'url' line in app.yaml by filling in the relevant placeholders.
    1. `gcloud app deploy`
1. Set up a Pub/Sub topic called my-topic.
1. Deploy the daily emailer script:
    1. Edit the `FROM_EMAIL` and `TO_EMAIL` lines in main.py. `FROM_EMAIL` should be the same email from the 'url' line in the email handler script, `TO_EMAIL` should be your personal email.
    1. Run `gcloud functions deploy ohlife_pubsub --runtime python37 --set-env-vars SENDGRID_API_KEY={YOUR_API_KEY} --trigger-topic my-topic`
1. Set up a Cloud Scheduler to trigger my-topic once every day.

