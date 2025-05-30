import os

from flask import Flask, redirect, render_template, send_from_directory, request, url_for

from .auth import login
from .database.handler import DatabaseHandler

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'loan_tracker.sqlite')
    )

    login_handler = login.Login()
    database_handler = DatabaseHandler()

    @app.get('/login')
    def login_get(error=""):
        return render_template('auth/login.html', error=login_handler.get_error_message())
    
    @app.post('/login')
    def login_post():
        username = request.form['username']
        password = request.form['password']
        login_handler.valid_login(username, password)
        login_handler.set_error("Wrong Username and/or Password.")
        return redirect(url_for('login_get'))

    @app.get('/init_db')
    def init_db():
        res = database_handler.init_database()
        return f"database {'initialized' if res else 'failed to initialize'}"

    @app.get('/favicon.ico')
    def get_favicaon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app
