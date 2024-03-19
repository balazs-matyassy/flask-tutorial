from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/method', methods=('GET', 'POST'))
def method():
    return render_template('method.html', method=request.method)


if __name__ == '__main__':
    app.run()
