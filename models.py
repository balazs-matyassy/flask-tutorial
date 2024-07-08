class Recipe:
    def __init__(self, recipe_id=None, category='', name='', difficulty=1):
        self.id = recipe_id
        self.category = category
        self.name = name
        self.difficulty = difficulty

    def update(self, data):
        if 'category' in data:
            self.category = data['category'].strip().capitalize()

        if 'name' in data:
            self.name = data['name'].strip().capitalize()

        if 'difficulty' in data:
            try:
                self.difficulty = int(data['difficulty'])

                if self.difficulty < 1:
                    self.difficulty = 1
                elif self.difficulty > 5:
                    self.difficulty = 5
            except ValueError:
                self.difficulty = 1

    def validate(self):
        errors = []

        if not self.category:
            errors.append('Category missing.')

        if not self.name:
            errors.append('Name missing.')

        return errors

    @staticmethod
    def create_from_row(row):
        if row:
            return Recipe(
                recipe_id=row['id'],
                category=row['category'],
                name=row['name'],
                difficulty=row['difficulty']
            )
        else:
            return None
