import dash
from dash import html, dcc

dash.register_page(__name__, path="/")


layout = html.Div(
    className="container mt-4",
    # Content Section
    children = html.Div(
        [
            html.H2("Welcome to our Home Monitoring System", className="mb-4"),
            html.P(
                "This site contains the monitoring of different rooms in the house.",
                className="lead",
            ),
        ],
        className="text-center",
    ),
)
