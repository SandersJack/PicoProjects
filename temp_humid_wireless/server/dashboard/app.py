import os
from flask import Flask, request, redirect, session
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user

import dash
from dash import dcc, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from utils.login_handler import restricted_page

import utils.Constants as Constants

import sqlite3
from flask_bcrypt import Bcrypt



# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)
secret_key = Constants.SECRET_KEY  # Replace 'your_secret_key' with a strong, random string
login_manager = LoginManager(server)

bcrypt = Bcrypt(server)

@server.route('/login', methods=['POST'])
def login_button_click():
    if request.form:
        username = request.form['username']
        password = request.form['password']
        if login_check(username, password):
            login_user(User(username))
            if 'url' in session:
                if session['url']:
                    url = session['url']
                    session['url'] = None
                    return redirect(url) ## redirect to target url
            return redirect('/') ## redirect to home
        else:
            with open('templates/error_page.html', 'r') as file:
                html_content = file.read()

            return html_content


external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
app = dash.Dash(
    __name__, server=server, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets, assets_folder='assets'
)
app.server.secret_key = secret_key

# Keep this out of source code repository - save in a file or a database
#  passwords should be encrypted

def login_check(username, password):
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
# Query the database for the user
    cursor.execute('SELECT username, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user and bcrypt.check_password_hash(user[1], password):
        return 1
    else:
        return 0



# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=secret_key)

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Div(id="user-status-header"),
        html.H1(children="Home Monitoring", 
                className="text-center display-4 mt-4 mb-4",
                style={'font-family': 'Arial, sans-serif', 'color': '#3498db'}),
        html.Hr(),
        html.Div(
            [
                dcc.Link("Home", href="/", className="btn btn-light mt-4 mb-4"),
                dcc.Link("Bedroom", href="/bedroom", className="btn btn-primary mr-2")
            ],
            className="text-center"
        ),
        dash.page_container,
        # Footer Section
        html.Footer(
            [
                html.P(
                    "© 2024 Home Monitoring System. All rights reserved.",
                    className="text-muted text-center mt-4",
                ),
            ],
            style={'background-color': '#2c3e50', 'color': '#ffffff', 'padding': '10px'}
        ),
    ], style={'background-color': '#2c3e50', 'color': '#ffffff', 'height': '100vh', 'overflow': 'hidden'}
)


@app.callback(
    Output("user-status-header", "children"),
    Output('url','pathname'),
    Input("url", "pathname"),
    Input({'index': ALL, 'type':'redirect'}, 'n_intervals')
)
def update_authentication_status(path, n):
    ### logout redirect
    if n:
        if not n[0]:
            return '', dash.no_update
        else:
            return '', '/login'

    ### test if user is logged in
    if current_user.is_authenticated:
        if path == '/login':
            return dcc.Link("logout", href="/logout", className="btn btn-danger"), '/'
        return dcc.Link("logout", href="/logout", className="btn btn-danger"), dash.no_update
    else:
        ### if page is restricted, redirect to login and save path
        if path in restricted_page:
            session['url'] = path
            return dcc.Link("login", href="/login",className="btn btn-success"), '/login'

    ### if path not login and logout display login link
    if current_user and path not in ['/login', '/logout']:
        return dcc.Link("login", href="/login",className="btn btn-success"), dash.no_update

    ### if path login and logout hide links
    if path in ['/login', '/logout']:
        return '', dash.no_update



if __name__ == "__main__":
    app.run_server(debug=False, port=5050)