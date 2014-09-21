from flask import request, Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def home():
    print('home')
    return render_template_string('home')


@app.route('/listen', methods=['POST'])
def listen():
    print('listen', request.form)
    return render_template_string('listen')

if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
