from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from models.user.user import User
from models.log import Log
import models.user.errors as errors

user_blueprint = Blueprint('users', __name__)  # file name


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    """
    Register a new user.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            User.register_user(username, password)
            # A session is a piece of data that is stored inside the app for each user different.
            session['username'] = username
            Log(username, 'Register.').save_to_mongo()
            flash('You have successfully registered.', 'success')
            return redirect(url_for('libors.index'))

        except errors.UserError as e:
            # Make the password strength error shorter.
            if e.message.startswith('A password must'):
                Log(username, 'Password strength error.').save_to_mongo()
            else:
                Log(username, e.message).save_to_mongo()
            flash(e.message, 'danger')
            return render_template('users/register.html')
    # If it's GET method, send user to the register page.
    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    """
    Log in a user.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            if User.is_login_valid(username, password):
                session['username'] = username
                Log(username, 'Login.').save_to_mongo()
                flash('You have successfully logged in.', 'success')
            return redirect(url_for('libors.index'))

        except errors.UserError as e:
            Log(username, e.message).save_to_mongo()
            flash(e.message, 'danger')
            return render_template('users/login.html')
    # If it's GET method, send user to the login page.
    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout():
    """
    Log out a user.
    """
    if not session.get('username'):
        message = 'You have not logged in.'
        Log('N/A', message).save_to_mongo()
        flash(message, 'danger')
        return redirect(url_for('.login_user'))

    Log(session['username'], 'Logout.').save_to_mongo()
    session['username'] = None

    flash('You are now logged out.', 'success')
    return redirect(url_for('.login_user'))
