from flask import g


class Recipe:
    def __init__(self, category='', name='', difficulty=1, recipe_id=None):
        self.id = recipe_id
        self.category = category
        self.name = name
        self.difficulty = difficulty

    @staticmethod
    def create(data):
        if not data:
            return None

        recipe = Recipe(recipe_id=data['id'])

        if 'category' in data:
            recipe.category = data['category'].strip().capitalize()

        if 'name' in data:
            recipe.name = data['name'].strip().capitalize()

        if 'difficulty' in data:
            try:
                recipe.difficulty = int(data['difficulty'])

                if recipe.difficulty < 1:
                    recipe.difficulty = 1
                elif recipe.difficulty > 5:
                    recipe.difficulty = 5
            except ValueError:
                recipe.difficulty = 1

        return recipe
