import dash
from dash import html, dcc


dash.register_page(__name__)

# Login screen
layout = html.Form(
    className="container",
    children=[
        html.H2("Please log in to continue", id="h1", className="mt-4 mb-4 text-center"),
        html.Div(
            className="row justify-content-center align-items-center",  # Center horizontally and vertically
            style={'height': '100vh'},  # Make the container full height
            children=[
                html.Div(
                    className="col-md-4",
                    children=[
                        dcc.Input(
                            placeholder="Enter your username",
                            type="text",
                            id="uname-box",
                            name="username",
                            className="form-control mb-3",
                        ),
                        dcc.Input(
                            placeholder="Enter your password",
                            type="password",
                            id="pwd-box",
                            name="password",
                            className="form-control mb-3",
                        ),
                        html.Button(
                            "Login",
                            n_clicks=0,
                            type="submit",
                            id="login-button",
                            className="btn btn-primary btn-block",
                        ),
                        html.Div("", id="output-state", className="mt-3 text-center")
                    ],
                ),
            ],
        ),
    ], method='POST'
)