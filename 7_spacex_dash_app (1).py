import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload, min_payload = spacex_df['Payload Mass (kg)'].max(), spacex_df['Payload Mass (kg)'].min()

# Initialize Dash app
app = dash.Dash(__name__)

def create_dropdown():
    """Create dropdown component for launch site selection."""
    return dcc.Dropdown(id='site-dropdown',
                        options=[
                            {'label': 'ALL SITES', 'value': 'ALL'},
                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                        ],
                        value='ALL',
                        placeholder="Select a Launch Site",
                        searchable=True)

def create_range_slider():
    """Create range slider component for payload selection."""
    return dcc.RangeSlider(id='payload-slider',
                           min=0, max=10000, step=1000,
                           value=[min_payload, max_payload],
                           marks={i: f'{i}' for i in range(0, 11000, 2500)})

def create_pie_chart():
    """Create pie chart component."""
    return dcc.Graph(id='success-pie-chart')

def create_scatter_chart():
    """Create scatter chart component."""
    return dcc.Graph(id='success-payload-scatter-chart')

# Define app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}),
    create_dropdown(),
    html.Br(),
    create_pie_chart(),
    html.Br(),
    html.P("Payload range (Kg):"),
    create_range_slider(),
    html.Br(),
    create_scatter_chart()
])

def generate_pie_chart(site):
    """Generate pie chart based on the selected site."""
    if site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class', title='Total Launches for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(filtered_df, names='class', title=f'Total Launches for {site}')
    return fig

def generate_scatter_chart(site, payload_range):
    """Generate scatter chart based on selected site and payload range."""
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    if site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]

    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                     color="Booster Version Category", title='Payload vs. Success')
    return fig

# Define callback for updating pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site_dropdown):
    return generate_pie_chart(site_dropdown)

# Define callback for updating scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(site_dropdown, payload_slider):
    return generate_scatter_chart(site_dropdown, payload_slider)

# Run app
if __name__ == '__main__':
    app.run_server()
