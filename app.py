from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['DB_HOST'] = 'localhost'
app.config['DB_PORT'] = 3306
app.config['DB_USERNAME'] = 'root'
app.config['DB_PASSWORD'] = 'password'
app.config['DB_DATABASE'] = 'flask_tutorial'

if __name__ == '__main__':
    app.run()

import routes
