import os

from flask import Flask, render_template, current_app

app = Flask(__name__)


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


def find_all():
    path = os.path.join(current_app.instance_path, 'recipes.txt')

    with open(path, encoding='utf-8') as file:
        recipes = []

        file.readline()  # header

        for line in file:
            recipe = Recipe.create_from_line(line)
            recipes.append(recipe)

        return recipes


@app.route('/')
def list_all():
    return render_template('list.html', recipes=find_all())


if __name__ == '__main__':
    app.run()
