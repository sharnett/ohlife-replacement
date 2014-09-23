ohlife-replacement
==================

ohlife was an email-based diary thing that shutdown in October 2014. This aims
to do basically the same thing.

You need an email address for this. I'm using gmail.

Create a file called email_credentials.py that looks like this:

```python
def email_credentials():
    mailhost = "smtp.gmail.com"
    fromaddr = "XXX@gmail.com"
    toaddrs = ["YYY"]
    credentials = ("XXX", "ZZZ")
    return mailhost, fromaddr, toaddrs, credentials
```

Make a sqlite3 database called db.db with one table:

```sql
create table entries (day date primary key, entry text);
```

Set up a web server to run listen.py. I'm just using the flask development
server inside a tmux session. I bought a $1.25 a month plan from ipxcore.

Sign up for an account at cloudmailin or equivalent. Basically you want
something that converts email to an http post. Send the http post to the
webserver in the previous step.

Set up a daily cron job to run ohlife.py.

When ohlife.py sends you an email, forward your response to the cloudmailin
email address.

Enjoy.
