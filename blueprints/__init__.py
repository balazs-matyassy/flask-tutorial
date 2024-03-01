from abc import ABC

from flask import request, session


class AbstractForm(ABC):
    def __init__(self, csrf_validation=False):
        self.csrf_validation = csrf_validation
        self.submitted = False
        self.errors = []

    @property
    def submitted_and_valid(self):
        return self.submitted and len(self.errors) == 0

    def validate_on_submit(self):
        if request.method != 'POST':
            return False

        self.submitted = True
        self.errors = []

        if self.csrf_validation and request.form.get('csrf_token') != session.get('csrf_token'):
            self.errors.append('Invalid CSRF token.')
            return False

        return True
