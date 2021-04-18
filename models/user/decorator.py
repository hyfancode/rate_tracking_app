from functools import wraps
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(fn: Callable) -> Callable:
    """
    Require users to log in to see the content.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            flash('You need to be signed in for this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return fn(*args, **kwargs)
    return wrapper


def requires_admin(fn: Callable) -> Callable:
    """
    Require Administrator account to see the content.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('username') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return fn(*args, **kwargs)
    return wrapper
