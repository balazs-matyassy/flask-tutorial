from flask import request

from blueprints import AbstractForm


class EntityForm(AbstractForm):
    def __init__(self, entity=None, fields=None, csrf_validation=False):
        super().__init__(csrf_validation)

        self.entity = entity
        self.fields = fields

    @property
    def create_form(self):
        return (self.entity is not None
                and self.entity.id is None)

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if self.entity:
            form = request.form

            if self.fields:
                form = {field: form[field] for field in self.fields}

            self.entity.form = form
            self.errors = self.entity.validate()

        return len(self.errors) == 0
