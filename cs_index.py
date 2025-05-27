from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from cs_app import cs_app

# Import components
from cs_map import create_map
from cs_histogram import create_histogram
from cs_controllers import DashboardControls

# Import data services
from services.data_service import CoralDataService

# Initialize components
controls = DashboardControls()
data_service = CoralDataService()

# =======================================
# Layout
# =======================================
app.layout = dbc.Container(
    fluid=True,
    children=[
        # Storage for cross-component communication
        dcc.Store(id='filtered-data-store'),
        dcc.Store(id='map-center-store', data={'lat': -8.052, 'lon': -34.928}),  # Default Recife coordinates
        
        # Control and Visualization Columns
        dbc.Row([
            # Left Column - Controls
            dbc.Col([
                controls.layout()
            ], md=3, className="controls-col"),
            
            # Right Column - Visualizations
            dbc.Col([
                dbc.Row(dbc.Col(create_map(), id="map-container", className="mb-4")),
                dbc.Row(dbc.Col(create_histogram(), id="histogram-container"))
            ], md=9)
        ])
    ],
    className="dashboard-container",
    style={'minHeight': '100vh'}
)

# =======================================
# Core Callbacks
# =======================================
@app.callback(
    Output('filtered-data-store', 'data'),
    [Input('date-range-store', 'data'),
     Input('locality-store', 'data'),
     Input('indicator-store', 'data')]
)
def update_filtered_data(date_range, localities, indicators):
    """Central data processing pipeline"""
    try:
        # Get base data
        df = data_service.get_combined_data()
        
        # Apply date filter
        if date_range and date_range.get('start') and date_range.get('end'):
            mask = (df['date'] >= date_range['start']) & (df['date'] <= date_range['end'])
            df = df[mask]
        
        # Apply locality filter
        if localities and 'selected' in localities and localities['selected'] != ['all']:
            df = df[df['locality_id'].isin(localities['selected'])]
        
        # Apply indicator-specific filters
        if indicators:
            # Add your indicator-specific filtering here
            pass
            
        return df.to_dict('records')
    
    except Exception as e:
        print(f"Data filtering error: {e}")
        return []

@app.callback(
    [Output('map-container', 'children'),
     Output('histogram-container', 'children'),
     Output('map-center-store', 'data')],
    [Input('filtered-data-store', 'data'),
     Input('indicator-store', 'data')],
    [State('map-center-store', 'data')]
)
def update_visualizations(filtered_data, indicators, current_center):
    """Update all visualizations when data or indicators change"""
    if not filtered_data:
        return [
            dbc.Alert("No data available for current filters", color="warning"),
            dbc.Alert("No data available for current filters", color="warning"),
            current_center
        ]
    
    try:
        df = pd.DataFrame(filtered_data)
        
        # Calculate new center if no data points exist
        if len(df) > 0:
            center = {
                'lat': df['latitude'].mean(),
                'lon': df['longitude'].mean()
            }
        else:
            center = current_center
        
        # Create visualizations
        map_fig = create_map(
            data=df,
            center=center,
            indicators=indicators
        )
        
        hist_fig = create_histogram(
            data=df,
            indicators=indicators
        )
        
        return [
            dcc.Graph(figure=map_fig, className="map-graph", config={'scrollZoom': True}),
            dcc.Graph(figure=hist_fig, className="hist-graph"),
            center
        ]
    
    except Exception as e:
        print(f"Visualization error: {e}")
        return [dbc.Alert("Error rendering visualizations", color="danger")] * 2 + [current_center]

# Register controller callbacks
controls.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)