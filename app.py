import os

from flask import Flask, redirect, render_template, send_from_directory, request, url_for

from loan_tracker.auth import Login, PasswordReset, Register
from loan_tracker.database import DatabaseHandler

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SESSION_COOKIE_SECURE = True,  # "limits cookies to HTTPS traffic only"
        SESSION_COOKIE_HTTPONLY = True,  # Disallows JS from reading the cookies
        SESSION_COOKIE_SAMESITE = 'Lax'  # Can either be 'Lax' or 'Strict'
    )

    database_handler = DatabaseHandler()
    auth_handler = Login(database_handler)

    @app.get('/')
    def index_get():
        # print(request.headers, flush=True)
        return render_template('index.html', url="http://localhost:5000")

    @app.get('/login')
    def login_get(error=""):
        return render_template('auth/login.html', error=auth_handler.get_error_message())
    
    @app.post('/login')
    def login_post():
        username = request.form['username']
        password = request.form['password']
        auth_handler.valid_login(username, password)
        auth_handler.set_error("Wrong Username and/or Password.")
        return redirect(url_for('login_get'))
    
    @app.get('/register')
    def register_get(error=""):
        return render_template('auth/register.html', error=auth_handler.get_error_message())
    
    @app.post('/register')
    def register_post():
        username = request.form['username']
        password = request.form['password']
        password = request.form['repeat_password']
        auth_handler.valid_login(username, password)
        auth_handler.set_error("Passwords do not match.")
        return redirect(url_for('register_post'))

    @app.get('/init_db')
    def init_db():
        res = database_handler.init_database()
        return f"database {'initialized' if res else 'failed to initialize'}"

    @app.get('/favicon.ico')
    def get_favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app
