from flask import render_template, abort, request, flash, redirect, url_for

from app import app
from models import Recipe
from repositories import RecipeRepository


@app.route('/')
def list_all():
    if request.args.get('search'):
        recipes = RecipeRepository.find_all_by_name_like(request.args.get('search'))
    else:
        recipes = RecipeRepository.find_all()

    return render_template('list.html', recipes=recipes)


@app.route('/view/<int:recipe_id>')
def view(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)

    return render_template('view.html', recipe=recipe)


@app.route('/create', methods=('GET', 'POST'))
def create():
    recipe = Recipe()
    errors = []

    if request.method == 'POST':
        recipe.update(request.form)
        errors = recipe.validate()

        if not errors:
            RecipeRepository.save(recipe)
            flash('Recipe created.')

            return redirect(url_for('list_all'))

    return render_template(
        'create.html',
        recipe=recipe,
        errors=errors
    )


@app.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
def edit(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    errors = []

    if request.method == 'POST':
        recipe.update(request.form)
        errors = recipe.validate()

        if not errors:
            RecipeRepository.save(recipe)
            flash('Recipe saved.')

            return redirect(url_for('edit', recipe_id=recipe_id))

    return render_template(
        'edit.html',
        recipe=recipe,
        errors=errors
    )


@app.route('/delete/<int:recipe_id>', methods=('POST',))
def delete(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    RecipeRepository.delete(recipe)
    flash('Recipe deleted.')

    return redirect(url_for('list_all'))
