from flask import Flask, render_template, request, session, g, redirect, url_for


def load_current_user():
    if session.get('user_id') is None:
        g.username = None
    else:
        g.username = load_users()[session.get('user_id')]


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

app.before_request(load_current_user)


@app.route('/', methods=('GET', 'POST'))
def home():
    users = load_users()

    if request.method == 'POST':
        user_id = int(request.form['user'])
        session['user_id'] = user_id
        session['username'] = users[user_id]

        return redirect(url_for('home'))

    return render_template('home.html', users=users)


@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('home'))


def load_users():
    with open('users.txt', encoding='utf-8') as file:
        return [line.strip() for line in file]


if __name__ == '__main__':
    app.run()
