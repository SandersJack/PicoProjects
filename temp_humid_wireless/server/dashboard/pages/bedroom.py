import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from dash import callback, no_update
from flask_login import current_user
import plotly.graph_objs as go
from utils.login_handler import require_login
from datetime import datetime, timedelta

dash.register_page(__name__)
require_login(__name__)

dark_template = "plotly_dark"

# Function to fetch data from the SQLite database
def fetch_data(start_time, end_time):
    conn = sqlite3.connect('data/sensor_data.db')
    cursor = conn.cursor()
    
    # Fetch data within the specified time range
    cursor.execute('SELECT * FROM sensor_data WHERE Timestamp BETWEEN ? AND ?', (start_time, end_time))
    rows = cursor.fetchall()
    
    conn.close()

    # Create a Pandas DataFrame from the fetched data
    columns = ['ID', 'Temperature', 'Humidity', 'Timestamp']
    df = pd.DataFrame(rows, columns=columns)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)

    return df

def layout():
    layout = html.Div(
        children=[
            html.H1("Sensor Data Dashboard"),
            
            # Dropdown to select temperature or humidity
            dcc.Dropdown(
                id='data-dropdown',
                options=[
                    {'label': 'Temperature', 'value': 'Temperature'},
                    {'label': 'Humidity', 'value': 'Humidity'}
                ],
                value='Temperature', className='dark-dropdown',
            ),

            dcc.DatePickerRange(
                id='date-range-picker',
                display_format='YYYY-MM-DD',
                start_date=(datetime.now() - timedelta(days=7)).date(), 
                end_date = datetime.now().date(),  # Initial end date (today)
                style={
                    'margin': '10px',
                    'border': '2px solid #4CAF50',
                    'border-radius': '8px',
                    'padding': '5px',
                    'background-color': '#f8f9fa',
                }
            ),

            # Graph to display temperature and humidity
            dcc.Graph(id='temperature-humidity-plot'),

        ]
    )
    return layout

# Define callback to update the graph based on dropdown selection
@callback(
    Output('temperature-humidity-plot', 'figure'),
    [Input('data-dropdown', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_plot(selected_data, start_date, end_date):
    start_time = datetime.strptime(start_date, '%Y-%m-%d')
    end_time = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Add one day to include the end date

    # Fetch data from the database within the specified time range
    df = fetch_data(start_time, end_time)

    df_resampled = df.resample('10T').mean()

    # Create a scatter plot using Plotly Express
    fig = px.scatter(
        df_resampled, 
        x=df_resampled.index, 
        y=selected_data, 
        title=f'{selected_data} Over Time',
        labels={'Timestamp': 'Time', selected_data: selected_data},
        template='plotly',
        color_discrete_sequence=['blue']
    ).update_layout(template=dark_template)

    fig.update_layout(
        title={'text': f'{selected_data} Over Time', 'x': 0.5},
        xaxis_title='Time',
        yaxis_title=selected_data,
        legend_title='Legend',
        margin=dict(l=0, r=0, t=50, b=50),
        hovermode='closest'
    )

    rolling_average = df_resampled[selected_data].rolling(window=3, center=True).mean()
    fig.add_trace(go.Scatter(x=rolling_average.index, y=rolling_average, mode='lines', name='Rolling Average'))

    return fig
