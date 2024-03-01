from flask import Flask, render_template, abort, request

from recipe import find_all_recipes, find_recipe_by_id, find_all_recipes_by_name_like

app = Flask(__name__)


@app.route('/')
def list_all_recipes():
    if request.args.get('search'):
        recipes = find_all_recipes_by_name_like(request.args.get('search'))
    else:
        recipes = find_all_recipes()

    return render_template('recipes_list.html', recipes=recipes)


@app.route('/view/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = find_recipe_by_id(recipe_id) or abort(404)

    return render_template('recipe_view.html', recipe=recipe)


if __name__ == '__main__':
    app.run()
