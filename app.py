from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from data.database import (
    get_locality_data,
    get_dafor_data,
    get_occ_data,
    get_management_data
)
import folium
from folium.plugins import MarkerCluster, Fullscreen
import pandas as pd
from branca.element import Template, MacroElement
import ast
from datetime import datetime

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load all data
def load_all_data():
    """Load and process all data tables"""
    locality = get_locality_data()
    dafor = get_dafor_data()
    occurrences = get_occ_data()
    management = get_management_data()
    
    # Process coordinate strings to lists
    for df in [locality, dafor, occurrences, management]:
        if 'coords' in ''.join(df.columns):
            coord_col = [c for c in df.columns if 'coords' in c][0]
            df[coord_col] = df[coord_col].apply(
                lambda x: ast.literal_eval(x) if pd.notnull(x) else None
            )
    
    return {
        'locality': locality,
        'dafor': dafor,
        'occurrences': occurrences,
        'management': management
    }

# Create initial map
def create_base_map(center=[-15, -50], zoom=5):
    """Create a base Folium map"""
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="cartodbpositron",
        control_scale=True
    )
    Fullscreen().add_to(m)
    return m

# Add layers to map
def add_locality_layer(m, locality_df):
    """Add locality data as polyline features"""
    feature_group = folium.FeatureGroup(name="Localidades")
    
    for _, row in locality_df.iterrows():
        if pd.notnull(row['coords_local']):
            folium.PolyLine(
                locations=row['coords_local'],
                color='blue',
                weight=2,
                popup=f"<b>Localidade:</b> {row['name']}<br>"
                      f"<b>ID:</b> {row['locality_id']}<br>"
                      f"<b>Data:</b> {row['date']}",
                tooltip=row['name']
            ).add_to(feature_group)
    
    feature_group.add_to(m)
    return m

def add_dafor_layer(m, dafor_df):
    """Add DAFOR data as circle markers"""
    marker_cluster = MarkerCluster(name="DAFOR")
    
    for _, row in dafor_df.iterrows():
        if pd.notnull(row['dafor_coords']):
            folium.CircleMarker(
                location=row['dafor_coords'][::-1],  # Reverse for [lat,lng]
                radius=5,
                color='red',
                fill=True,
                popup=f"<b>DAFOR ID:</b> {row['dafor_id']}<br>"
                      f"<b>Valor:</b> {row['dafor_value']}<br>"
                      f"<b>Data:</b> {row['date']}",
                tooltip=f"DAFOR {row['dafor_id']}"
            ).add_to(marker_cluster)
    
    marker_cluster.add_to(m)
    return m

def add_occurrence_layer(m, occ_df):
    """Add occurrence data as markers"""
    feature_group = folium.FeatureGroup(name="Ocorrências")
    
    for _, row in occ_df.iterrows():
        if pd.notnull(row['spot_coords']):
            folium.Marker(
                location=row['spot_coords'][::-1],  # Reverse for [lat,lng]
                icon=folium.Icon(color='green', icon='info-sign'),
                popup=f"<b>Ocorrência ID:</b> {row['occurrence_id']}<br>"
                      f"<b>Profundidade:</b> {row['depth']}<br>"
                      f"<b>Data:</b> {row['date']}",
                tooltip=f"Ocorrência {row['occurrence_id']}"
            ).add_to(feature_group)
    
    feature_group.add_to(m)
    return m

def add_management_layer(m, mgmt_df):
    """Add management data as custom icons"""
    feature_group = folium.FeatureGroup(name="Manejo")
    
    for _, row in mgmt_df.iterrows():
        if pd.notnull(row['management_coords']):
            folium.Marker(
                location=row['management_coords'][::-1],  # Reverse for [lat,lng]
                icon=folium.Icon(color='orange', icon='scissors', prefix='fa'),
                popup=f"<b>Manejo ID:</b> {row['management_id']}<br>"
                      f"<b>Massa:</b> {row['managed_mass_kg']} kg<br>"
                      f"<b>Observador:</b> {row['observer']}<br>"
                      f"<b>Data:</b> {row['date']}",
                tooltip=f"Manejo {row['management_id']}"
            ).add_to(feature_group)
    
    feature_group.add_to(m)
    return m

# Create sidebar controls
def create_controls():
    return html.Div([
        html.H4("Controles do Mapa", className="mb-3"),
        dbc.Accordion([
            dbc.AccordionItem([
                dcc.Checklist(
                    id='localidade-toggle',
                    options=[{'label': ' Mostrar Localidades', 'value': 'show'}],
                    value=['show'],
                    labelStyle={'display': 'block'}
                ),
                dcc.Checklist(
                    id='dafor-toggle',
                    options=[{'label': ' Mostrar DAFOR', 'value': 'show'}],
                    value=['show'],
                    labelStyle={'display': 'block'}
                ),
                dcc.Checklist(
                    id='occurrence-toggle',
                    options=[{'label': ' Mostrar Ocorrências', 'value': 'show'}],
                    value=['show'],
                    labelStyle={'display': 'block'}
                ),
                dcc.Checklist(
                    id='management-toggle',
                    options=[{'label': ' Mostrar Manejo', 'value': 'show'}],
                    value=['show'],
                    labelStyle={'display': 'block'}
                ),
            ], title="Camadas"),
            
            dbc.AccordionItem([
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=datetime(2010, 1, 1),
                    max_date_allowed=datetime.today(),
                    start_date=datetime(2020, 1, 1),
                    end_date=datetime.today(),
                    display_format='DD/MM/YYYY'
                )
            ], title="Filtro Temporal")
        ], start_collapsed=False)
    ], className="p-3 border rounded")

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(create_controls(), width=3),
        dbc.Col([
            html.Iframe(
                id='map-iframe',
                style={'width': '100%', 'height': '85vh', 'border': 'none'}
            ),
            dcc.Store(id='map-center-store', data={'lat': -15, 'lng': -50}),
            dcc.Store(id='map-zoom-store', data=5)
        ], width=9)
    ])
], fluid=True)

# Callbacks
@app.callback(
    Output('map-iframe', 'srcDoc'),
    Output('map-center-store', 'data'),
    Output('map-zoom-store', 'data'),
    Input('localidade-toggle', 'value'),
    Input('dafor-toggle', 'value'),
    Input('occurrence-toggle', 'value'),
    Input('management-toggle', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    State('map-center-store', 'data'),
    State('map-zoom-store', 'data')
)
def update_map(
    show_localidade, show_dafor, show_occurrence, show_management,
    start_date, end_date, center_data, zoom_data
):
    # Load data
    data = load_all_data()
    
    # Create base map with preserved center/zoom
    center = [center_data['lat'], center_data['lng']]
    m = create_base_map(center, zoom_data)
    
    # Apply date filtering
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Add layers based on selections
    if 'show' in show_localidade:
        filtered_locality = data['locality'][
            (data['locality']['date'] >= start_date) & 
            (data['locality']['date'] <= end_date)
        ]
        m = add_locality_layer(m, filtered_locality)
    
    if 'show' in show_dafor:
        filtered_dafor = data['dafor'][
            (data['dafor']['date'] >= start_date) & 
            (data['dafor']['date'] <= end_date)
        ]
        m = add_dafor_layer(m, filtered_dafor)
    
    if 'show' in show_occurrence:
        filtered_occ = data['occurrences'][
            (data['occurrences']['date'] >= start_date) & 
            (data['occurrences']['date'] <= end_date)
        ]
        m = add_occurrence_layer(m, filtered_occ)
    
    if 'show' in show_management:
        filtered_mgmt = data['management'][
            (data['management']['date'] >= start_date) & 
            (data['management']['date'] <= end_date)
        ]
        m = add_management_layer(m, filtered_mgmt)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Get current map view (for persistence)
    current_center = m.get_center()
    current_zoom = m.get_zoom()
    
    return (
        m._repr_html_(),
        {'lat': current_center[0], 'lng': current_center[1]},
        current_zoom
    )

if __name__ == '__main__':
    app.run(debug=True)