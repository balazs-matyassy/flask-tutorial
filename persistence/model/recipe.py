from persistence.model import AbstractEntity
from persistence.utils import try_parse_int


class Recipe(AbstractEntity):
    def __init__(self, category='', name='', description='', difficulty=1, recipe_id=None):
        self.id = recipe_id
        self.category = category
        self.name = name
        self.description = description
        self.difficulty = difficulty

    @property
    def difficulty_description(self):
        if self.difficulty == 1:
            return 'Very easy'
        elif self.difficulty == 2:
            return 'Easy'
        elif self.difficulty == 3:
            return 'Medium'
        elif self.difficulty == 4:
            return 'Difficult'
        elif self.difficulty == 5:
            return 'Very difficult'

        return 'Unknown'

    @property
    def form(self):
        return {
            'id': self.id,
            'category': self.category,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty
        }

    @form.setter
    def form(self, data):
        if 'category' in data:
            self.category = data['category'].strip().capitalize()

        if 'name' in data:
            self.name = data['name'].strip().capitalize()

        if 'description' in data:
            self.description = data['description'].strip()

        if 'difficulty' in data:
            self.difficulty = try_parse_int(data['difficulty'], 1, 1, 5)

    def update(self, data):
        self.form = data

    def validate(self):
        errors = []

        if not self.category:
            errors.append('Category missing.')

        if not self.name:
            errors.append('Name missing.')

        return errors

    @staticmethod
    def create(data):
        if not data:
            return None

        recipe = Recipe(recipe_id=data['id'])
        recipe.update(data)

        return recipe

    def __repr__(self):
        return f'<Recipe {self.name}>'
