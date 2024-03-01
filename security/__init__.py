from flask import g, session

from persistence.repository.user import UserRepository


def init_app(app):
    app.before_request(__load_current_user)
    app.jinja_env.globals['is_fully_authenticated'] = lambda: g.user is not None
    app.jinja_env.globals['is_admin'] = lambda: g.user is not None and g.user.admin
    app.jinja_env.globals['csrf_token'] = lambda: session['csrf_token']


def __load_current_user():
    if not session.get('user_id'):
        g.user = None
    else:
        g.user = UserRepository.find_by_id(session.get('user_id'))
