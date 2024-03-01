class Recipe:
    def __init__(self, category='', name='', difficulty=1, recipe_id=None):
        self.id = recipe_id
        self.category = category
        self.name = name
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
            'difficulty': self.difficulty
        }

    @form.setter
    def form(self, data):
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

    def to_line(self):
        return f'{self.id}\t{self.category}\t{self.name}\t{self.difficulty}'

    @staticmethod
    def create(line):
        values = line.strip().split('\t')

        return Recipe(
            recipe_id=int(values[0].strip()),
            category=values[1].strip(),
            name=values[2].strip(),
            difficulty=int(values[3].strip())
        )


def find_all_recipes():
    with open('recipes.txt', encoding='utf-8') as file:
        recipes = []

        file.readline()  # header

        for line in file:
            recipe = Recipe.create(line)
            recipes.append(recipe)

        return recipes


def find_recipe_by_id(recipe_id):
    for recipe in find_all_recipes():
        if recipe.id == recipe_id:
            return recipe

    return None


def find_all_recipes_by_name_like(name):
    recipes = []

    for recipe in find_all_recipes():
        if name.lower() in recipe.name.lower():
            recipes.append(recipe)

    return recipes


def save_recipe(recipe):
    recipes = find_all_recipes()

    if not recipe.id:
        max_id = 0

        for i in range(len(recipes)):
            if recipes[i].id > max_id:
                max_id = recipes[i].id

        recipe.id = max_id + 1
        recipes.append(recipe)
    else:
        for i in range(len(recipes)):
            if recipes[i].id == recipe.id:
                recipes[i] = recipe
                break

    __store_all_recipes(recipes)

    return recipe


def delete_recipe_by_id(recipe_id):
    recipes = find_all_recipes()

    for i in range(len(recipes)):
        if recipes[i].id == recipe_id:
            recipes.pop(i)
            break

    __store_all_recipes(recipes)


def __store_all_recipes(recipes):
    with open('recipes.txt', 'w', encoding='utf-8') as file:
        file.write('id\tcategory\tname\tdifficulty\n')

        for recipe in sorted(recipes, key=lambda item: f'{item.category}\0{item.name}'):
            file.write(f'{recipe.to_line()}\n')
