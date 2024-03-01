
from flask import render_template, abort, flash, redirect, url_for, request, session

from blueprints.forms import EntityForm
from blueprints.users import bp
from persistence.model.user import User
from persistence.repository.user import UserRepository
from security.decorators import is_admin


@bp.route('/')
@is_admin
def list_all():
    if request.args.get('search'):
        users = UserRepository.find_all_by_username_like(request.args.get('search'))
    else:
        users = UserRepository.find_all()

    return render_template('users/list.html', users=users)


@bp.route('/create', methods=('GET', 'POST'))
@is_admin
def create():
    user = User()
    form = EntityForm(user, csrf_validation=True)

    if form.validate_on_submit():
        try:
            UserRepository.save(user)
            flash('User created.')

            return redirect(url_for('users.list_all'))
        except Exception as err:
            flash(str(err))

    return render_template('users/form.html', form=form)


@bp.route('/edit/<int:user_id>', methods=('GET', 'POST'))
@is_admin
def edit(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)
    form = EntityForm(user, csrf_validation=True)

    if form.validate_on_submit():
        try:
            UserRepository.save(user)
            flash('User saved.')

            return redirect(url_for('users.edit', user_id=user.id))
        except Exception as err:
            flash(str(err))

    return render_template('users/form.html', form=form)


@bp.route('/delete/<int:user_id>', methods=('POST',))
@is_admin
def delete(user_id):
    UserRepository.find_by_id(user_id) or abort(404)
    csrf = EntityForm(csrf_validation=True)

    if not csrf.validate_on_submit():
        for error in csrf.errors:
            flash(error)
    else:
        try:
            UserRepository.delete_by_id(user_id)
            flash('User deleted.')
        except Exception as err:
            flash(str(err))

    return redirect(url_for('users.list_all'))
