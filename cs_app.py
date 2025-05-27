from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from cs_controls import controls
from cs_map import create_map
from cs_histogram import create_histogram

# Import your data service
from services.data_services import CoralDataService

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize data service
data_service = CoralDataService()

# Load data function
def load_data():
    try:
        print("Loading data from database...")
        df = data_service.get_combined_data()
        print(f"Successfully loaded {len(df)} records")
        print("Columns:", df.columns.tolist())
        return df
    except Exception as e:
        print("Error loading data:", str(e))
        return pd.DataFrame()  # Return empty DataFrame if error

# Load initial data
df = load_data()

# Rest of your app layout and callbacks remain the same...
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(controls, md=3, style={'padding': '20px'}),
        dbc.Col([
            dcc.Graph(id='map', figure=create_map(df)),
            dcc.Graph(id='histogram', figure=create_histogram(df))
        ], md=9)
    ]),
 html.Div(id='debug-output', style={'marginTop': '20px'}),   
], fluid=True)

@app.callback(
    [Output('map', 'figure'),
     Output('histogram', 'figure')],
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('locality-dropdown', 'value')]
)
def update_figures(start_date, end_date, localities):
    filtered_df = df.copy()  # Start with all data
    
    # Add simple filtering
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date'] >= start_date) & 
            (filtered_df['date'] <= end_date)
        ]
    
    if localities and localities != ['all']:
        filtered_df = filtered_df[filtered_df['locality_id'].isin(localities)]
    
    return create_map(filtered_df), create_histogram(filtered_df)

############### debusg output for map data
@app.callback(
    Output('debug-output', 'children'),
    Input('map', 'figure')
)
def show_map_data(fig):
    if fig is None or 'data' not in fig:
        return "No figure data available"
    
    # Extract coordinates from the map data
    map_data = fig['data'][0]
    return html.Pre(f"""
    Map Data Status:
    Latitude points: {len(map_data.get('lat', []))}
    Longitude points: {len(map_data.get('lon', []))}
    Hover names: {len(map_data.get('hovertext', []))}
    """)





##########

if __name__ == '__main__':
    app.run(debug=True)