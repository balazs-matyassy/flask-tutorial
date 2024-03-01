import functools

from flask import redirect, url_for, request, g, abort


def is_fully_authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('security.login', redirect=request.path))

        return view(**kwargs)

    return wrapped_view


def is_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('security.login', redirect=request.path))
        elif not g.user.admin:
            abort(401)

        return view(**kwargs)

    return wrapped_view
