import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from dash import callback, no_update

# Function to fetch data from the SQLite database
def fetch_data():
    conn = sqlite3.connect('data/sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensor_data')
    rows = cursor.fetchall()
    conn.close()

    # Create a Pandas DataFrame from the fetched data
    columns = ['ID', 'Temperature', 'Humidity', 'Timestamp']
    df = pd.DataFrame(rows, columns=columns)
    return df

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['style/main.css'])

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1("Sensor Data Dashboard"),
        
        # Dropdown to select temperature or humidity
        dcc.Dropdown(
            id='data-dropdown',
            options=[
                {'label': 'Temperature', 'value': 'Temperature'},
                {'label': 'Humidity', 'value': 'Humidity'}
            ],
            value='Temperature'
        ),

        # Graph to display temperature and humidity
        dcc.Graph(id='temperature-humidity-plot'),

        # Interval component for auto-updating every 1 minute (60000 milliseconds)
        dcc.Interval(
            id='interval-component',
            interval=60000,  # in milliseconds
            n_intervals=0
        )
    ],
)

# Define callback to update the graph based on dropdown selection
@app.callback(
    Output('temperature-humidity-plot', 'figure'),
    [Input('data-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_plot(selected_data, n_intervals):
    # Fetch data from the database
    df = fetch_data()

    # Create a scatter plot using Plotly Express
    fig = px.scatter(
        df, 
        x='Timestamp', 
        y=selected_data, 
        title=f'{selected_data} Over Time',
        labels={'Timestamp': 'Time', selected_data: selected_data},
        template='plotly',
        color_discrete_sequence=['blue']
    )

    fig.update_layout(
        title={'text': f'{selected_data} Over Time', 'x': 0.5},
        xaxis_title='Time',
        yaxis_title=selected_data,
        legend_title='Legend',
        margin=dict(l=0, r=0, t=50, b=50),
        hovermode='closest'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5050)