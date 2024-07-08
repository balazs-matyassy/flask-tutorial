from flask import render_template, abort, request

from app import app
from repositories import RecipeRepository


@app.route('/')
def list_all():
    if request.args.get('search'):
        recipes = RecipeRepository.find_all_by_name_like(request.args.get('search'))
    else:
        recipes = RecipeRepository.find_all()

    return render_template('list.html', recipes=recipes)


@app.route('/<int:recipe_id>')
def view(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)

    return render_template('view.html', recipe=recipe)
