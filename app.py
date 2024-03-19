from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def home():
    order = None
    summary = False

    if request.method == 'POST':
        order = {
            'product': request.form['product'],
            'quantity': int(request.form['quantity'])
        }

        summary = True

    return render_template('home.html', order=order, summary=summary)


@app.route('/view-state', methods=('GET', 'POST'))
def view_state():
    order = {
        'product': 'Androids',
        'quantity': 1
    }
    summary = False

    if request.method == 'POST':
        order['product'] = request.form['product']
        order['quantity'] = int(request.form['quantity'])
        summary = True

    return render_template('view_state.html', order=order, summary=summary)


if __name__ == '__main__':
    app.run()
