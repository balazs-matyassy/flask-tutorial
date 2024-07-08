import functools

from flask import session, redirect, url_for


def is_authenticated_fully(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
