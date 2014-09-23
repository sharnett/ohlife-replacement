import re
import sqlite3
from flask import request, Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def home():
    return render_template_string('home')


@app.route('/listen', methods=['POST'])
def listen():
    subject = request.form.get('headers[Subject]')
    body = request.form.get('plain')

    def extract_day(s):
        pattern = r'(\d\d\d\d-\d\d-\d\d)'
        m = re.search(pattern, s)
        if m is not None:
            return m.group(1)
    day = extract_day(subject)

    def extract_entry(body):
        entry_lines = []
        for line in body.split('\n'):
            if 'Forwarded message' in line:
                break
            entry_lines.append(line)
        return ''.join(entry_lines)
    entry = extract_entry(body)

    print(day)
    print(entry)

    write_to_db(day, entry)

    return render_template_string('listen')


def write_to_db(day, entry):
    if day is not None and entry is not None:
        try:
            with sqlite3.connect('db.db') as db:
                query = 'insert into entries (day, entry) values (?, ?)'
                db.execute(query, (day, entry))
                db.commit()
            print('successfully wrote to db')
        except:
            print('ERROR: failed to write to db')
            raise

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
