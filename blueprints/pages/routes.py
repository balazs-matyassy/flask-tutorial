from flask import render_template, g, flash, redirect, url_for

from blueprints.pages import bp
from blueprints.pages.forms import ChangePasswordForm
from persistence.repository.user import UserRepository
from security.decorators import is_fully_authenticated


@bp.route('/')
def home():
    return render_template('pages/home.html')


@bp.route('/profile', methods=('GET', 'POST'))
@is_fully_authenticated
def profile():
    user = g.user
    form = ChangePasswordForm(user, csrf_validation=True)

    if form.validate_on_submit():
        try:
            UserRepository.save(user)
            flash('Password changed successfully!')

            return redirect(url_for('pages.profile'))
        except Exception as err:
            flash(str(err))

    return render_template('pages/profile.html', form=form)
