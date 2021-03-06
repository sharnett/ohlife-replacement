ohlife-replacement
==================

ohlife was an email-based diary thing that shut down in October 2014. This aims
to do basically the same thing.

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

Enjoy.
