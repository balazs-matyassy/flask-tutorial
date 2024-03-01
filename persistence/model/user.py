from werkzeug.security import generate_password_hash, check_password_hash

from persistence.model import AbstractEntity


class User(AbstractEntity):
    def __init__(self, username='', digest=None, admin=False, user_id=None):
        self.id = user_id
        self.username = username
        self.digest = digest
        self.admin = admin

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        if value and len(value) > 0:
            self.digest = generate_password_hash(value)

    @property
    def form(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.digest,
            'admin': self.admin
        }

    @form.setter
    def form(self, data):
        if 'username' in data:
            self.username = data['username'].strip().lower()

        if 'password' in data:
            self.password = data['password']

        self.admin = 'role' in data and str(data['role']) == '1'

    def check_password(self, password):
        return check_password_hash(self.digest, password)

    def update(self, data):
        if 'username' in data:
            self.username = data['username'].strip().lower()

        if 'digest' in data:
            self.digest = data['digest']

        if 'password' in data:
            self.password = data['password']

        self.admin = 'role' in data and str(data['role']) == '1'

    def validate(self):
        errors = []

        if not self.username:
            errors.append('Username missing.')

        if not self.digest:
            errors.append('Password missing.')

        return errors

    @staticmethod
    def create(data):
        if data is None:
            return None

        user = User(user_id=data.get('id'))
        user.update(data)

        return user

    def __repr__(self):
        return f'<User {self.username}>'
