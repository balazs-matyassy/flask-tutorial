class Recipe:
    def __init__(self, recipe_id=None, category='', name='', difficulty=1):
        self.id = recipe_id
        self.category = category
        self.name = name
        self.difficulty = difficulty

    @staticmethod
    def create_from_line(line):
        values = line.strip().split('\t')

        return Recipe(
            recipe_id=int(values[0].strip()),
            category=values[1].strip(),
            name=values[2].strip(),
            difficulty=int(values[3].strip())
        )
