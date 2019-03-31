import argparse
import datetime
import itertools

import arrow
from google.cloud import datastore
import pandas as pd

_MAX_BATCH_SIZE = 400

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def batch_upsert(client, csv_filename):
    df = pd.read_csv(csv_filename).dropna()
    tasks = []
    for _, row in df.iterrows():
        date = datetime.datetime.strptime(row.date, '%Y-%m-%d')
        if basic_query(client, date):
            print('already have entry for %s' % date)
            continue

        task = datastore.Entity(client.key('DailyEntry'))

        task.update({
            'date': datetime.datetime.strptime(row.date, '%Y-%m-%d'),
            'entry': unicode(row.entry, 'utf-8')
        })

        tasks.append(task)

    # [START datastore_batch_upsert]
    for batch in grouper(tasks, 400):
        client.put_multi([task for task in batch if task is not None])
    # [END datastore_batch_upsert]


def basic_query(client, date=None):
    # [START datastore_basic_query]
    if date is None:
        date = datetime.datetime.strptime('2019-04-03', '%Y-%m-%d')
    query = client.query(kind='DailyEntry')
    query.add_filter('date', '=', date)
    # [END datastore_basic_query]

    return list(query.fetch())

def dedupe(client, start_date='2011-08-05'):
    date = arrow.get(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    while date < end_date:
        query = client.query(kind='DailyEntry')
        query.add_filter('date', '=', date.datetime)
        result = list(query.fetch())
        date = date.replace(days=1)
        if len(result) == 0:
            continue
        print(len(result), str(date.date()))
        if len(result) > 1:
            key = client.key('DailyEntry', result[0].id)
            client.delete(key)

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

def main(project_id):
    client = datastore.Client(project_id)

    # dedupe(client)
    # batch_upsert(client, CSV_FILENAME)
    # print(basic_query(client))
    print(_get_entry())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do stuff')
    parser.add_argument('project_id', help='Your cloud project ID.')

    args = parser.parse_args()

    main(args.project_id)