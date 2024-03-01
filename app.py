from flask import Flask, render_template

app = Flask(__name__)


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


@app.route('/')
def list_all_recipes():
    return render_template('recipes_list.html', recipes=find_all_recipes())


if __name__ == '__main__':
    app.run()
