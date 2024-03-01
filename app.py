from flask import Flask, render_template

app = Flask(__name__)


def find_all_recipes():
    with open('recipes.txt', encoding='utf-8') as file:
        recipes = []

        file.readline()  # header

        for line in file:
            values = line.strip().split('\t')

            recipe = {
                'id': int(values[0]),
                'category': values[1],
                'name': values[2],
                'difficulty': int(values[3])
            }
            recipes.append(recipe)

        return recipes


@app.route('/')
def list_all_recipes():
    return render_template('recipes_list.html', recipes=find_all_recipes())


if __name__ == '__main__':
    app.run()
