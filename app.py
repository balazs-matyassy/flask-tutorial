from flask import Flask, render_template, abort, request, flash, redirect, url_for

from recipe import (Recipe, find_all_recipes, find_recipe_by_id, find_all_recipes_by_name_like,
                    save_recipe, delete_recipe_by_id)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # flash üzenetekhez kell


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


@app.route('/create', methods=('GET', 'POST'))
def create_recipe():
    recipe = Recipe()
    errors = []

    if request.method == 'POST':
        recipe.form = request.form
        errors = recipe.validate()

        if not errors:
            save_recipe(recipe)
            flash('Recipe created.')

            return redirect(url_for('list_all_recipes'))

    return render_template(
        'recipe_form.html',
        recipe=recipe,
        errors=errors
    )


@app.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
def edit_recipe(recipe_id):
    recipe = find_recipe_by_id(recipe_id) or abort(404)
    errors = []

    if request.method == 'POST':
        recipe.form = request.form
        errors = recipe.validate()

        if not errors:
            save_recipe(recipe)
            flash('Recipe saved.')

            return redirect(url_for('edit_recipe', recipe_id=recipe.id))

    return render_template(
        'recipe_form.html',
        recipe=recipe,
        errors=errors
    )


@app.route('/delete/<int:recipe_id>', methods=('POST',))
def delete_recipe(recipe_id):
    find_recipe_by_id(recipe_id) or abort(404)
    delete_recipe_by_id(recipe_id)
    flash('Recipe deleted.')

    return redirect(url_for('list_all_recipes'))


if __name__ == '__main__':
    app.run()
