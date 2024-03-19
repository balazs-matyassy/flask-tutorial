from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        return {
            'product': request.form['product'],
            'quantity': int(request.form['quantity'])
        }

    return render_template('home.html')


if __name__ == '__main__':
    app.run()
