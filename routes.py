import json
import os

from flask import render_template, abort, request, flash, redirect, url_for, session, current_app

from app import app
from models import Recipe
from repositories import RecipeRepository
from security import is_authenticated_fully


@app.route('/login', methods=('GET', 'POST'))
def login():
    if session.get('username'):
        return redirect(url_for('list_all_recipes'))

    username = ''
    password = ''
    errors = []

    if request.method == 'POST':
        path = os.path.join(current_app.instance_path, 'users.json')

        with open(path, encoding='utf-8') as file:
            users = json.load(file)

        username = request.form['username'].strip().lower()
        password = request.form['password']

        if not username:
            errors.append('Username missing.')

        if not password:
            errors.append('Password missing.')

        if not errors and (username not in users or users[username] != password):
            errors.append('Invalid username or password.')

        if not errors:
            session['username'] = username
            flash('Login successful.')

            return redirect(url_for('list_all'))

    return render_template(
        'login.html',
        username=username,
        password=password,
        errors=errors
    )


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('list_all'))


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
@is_authenticated_fully
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
@is_authenticated_fully
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
