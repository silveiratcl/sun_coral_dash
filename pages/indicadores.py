import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import ast
import datetime
import folium
from folium.plugins import Fullscreen
from branca.element import Template, MacroElement
from flask_caching import Cache
import os

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Configure cache
cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

# --- Database Connection ---
@cache.memoize(timeout=3600)
def init_connection():
    try:
        # Replace with your actual connection details
        connection_details = {
            "dialect": "postgresql",
            "driver": "psycopg2",
            "username": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_NAME")
        }
        
        encoded_password = quote_plus(connection_details["password"])
        connection_string = (
            f"{connection_details['dialect']}+{connection_details['driver']}://"
            f"{connection_details['username']}:{encoded_password}@"
            f"{connection_details['host']}:{connection_details['port']}/"
            f"{connection_details['database']}"
        )
        engine = create_engine(connection_string)
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return engine
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

engine = init_connection()

# --- Data Fetching Functions ---
@cache.memoize(timeout=3600)
def get_management_data():
    query = "SELECT management_id, management_coords, observer, managed_mass_kg, date FROM data_coralsol_management"
    with engine.begin() as connection:
        df = pd.read_sql(query, con=connection.connection)
    df.columns = map(str.lower, df.columns)
    return df

@cache.memoize(timeout=3600)
def get_locality_data():
    query = "SELECT locality_id, coords_local, name, date FROM data_coralsol_locality"
    with engine.begin() as connection:
        df = pd.read_sql(query, con=connection.connection)
    df.columns = map(str.lower, df.columns)
    return df

@cache.memoize(timeout=3600)
def get_occ_data():
    query = "SELECT Occurrence_id, Spot_coords, Date, Depth, Superficie_photo FROM data_coralsol_occurrence WHERE Superficie_photo IS NOT NULL LIMIT 10"
    with engine.begin() as connection:
        df = pd.read_sql(query, con=connection.connection)
    df.columns = map(str.lower, df.columns)
    return df

@cache.memoize(timeout=3600)
def get_dafor_data():
    query = "SELECT Dafor_id, Locality_id, Dafor_coords, Date, Horizontal_visibility, Bathymetric_zone, Method, Dafor_value FROM data_coralsol_dafor"
    with engine.begin() as connection:
        df = pd.read_sql(query, con=connection.connection)
    df.columns = map(str.lower, df.columns)
    return df

# --- Map Utilities ---
def create_folium_map(center=None, zoom=None):
    if center is None:
        center = [-27.281798, -48.366133]
    if zoom is None:
        zoom = 13
    
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2lsdmVpcmF0Y2wiLCJhIjoiY202MTRrN3N5MGt3MDJqb2xhc3R0empqZCJ9.YfjBqq5HbnacUNw9Tyiaew",
        attr="Mapbox attribution",
        max_zoom=20,
        min_zoom=1
    )
    Fullscreen().add_to(m)
    return m

# Legend templates (same as your Streamlit version)
legend_transect = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>     
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: red; opacity: 0.75;'></span>ALTO (>30)</li>
    <li><span style='background: orange; opacity: 0.75;'></span>MODERADO (15-30)</li>
    <li><span style='background: yellow; opacity: 0.75;'></span> BAIXO (5-15) </li>
    <li><span style='background: green; opacity: 0.75;'></span> AUSENTE </li>
  </ul>
</div>
</div> 
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>
{% endmacro %}
"""

legend_effort = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>     
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: red; opacity: 0.75;'></span>ALTO (>300 min.)</li>
    <li><span style='background: orange; opacity: 0.75;'></span>MODERADO (150-300 min.)</li>
    <li><span style='background: yellow; opacity: 0.75;'></span> BAIXO (50-150 min.) </li>
    <li><span style='background: green; opacity: 0.75;'></span> MUITO BAIXO (0-50 min.) </li>
  </ul>
</div>
</div> 
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>
{% endmacro %}
"""

# --- App Layout ---
app.layout = html.Div([
    dcc.Store(id='map-center-store', data={'lat': -27.281798, 'lng': -48.366133}),
    dcc.Store(id='map-zoom-store', data=13),
    
    html.Div([
        html.Img(src='./assets/logo_horiz.png', style={'height': '60px'}),
        html.H1("Indicadores do Monitoramento", style={'margin-left': '20px'})
    ], style={'display': 'flex', 'align-items': 'center', 'padding': '10px'}),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Filtros", className="card-title"),
                    dcc.DatePickerRange(
                        id='date-range',
                        min_date_allowed=datetime.date(2012, 1, 1),
                        max_date_allowed=datetime.date.today() + datetime.timedelta(days=1),
                        start_date=datetime.date(2012, 1, 1),
                        end_date=datetime.date.today(),
                        display_format='DD/MM/YYYY'
                    ),
                    html.Hr(),
                    dbc.RadioItems(
                        id='indicator-selector',
                        options=[
                            {"label": "Transectos com Coral-sol", "value": "transectos"},
                            {"label": "Esforço de Monitoramento", "value": "esforco"},
                            {"label": "Detecções por ano", "value": "detect_ano"},
                            {"label": "Detecções vs. Massa Manejada", "value": "detect_massa"}
                        ],
                        value="transectos",
                        inline=False
                    )
                ])
            ], style={'height': '100%'})
        ], width=3),
        
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(
                    html.Div([
                        html.Iframe(
                            id='folium-map',
                            style={'width': '100%', 'height': '700px', 'border': 'none'}
                        ),
                        dbc.Button("Atualizar Mapa", id='update-map-btn', className="mt-2")
                    ]),
                    label="Mapa",
                    id='map-tab'
                ),
                dbc.Tab(
                    html.Div(id='chart-container'),
                    label="Gráficos",
                    id='chart-tab'
                )
            ]),
            
            html.Div(id='data-table-container')
        ], width=9)
    ])
])

# --- Callbacks ---
@app.callback(
    Output('folium-map', 'srcDoc'),
    Output('data-table-container', 'children'),
    Output('map-center-store', 'data'),
    Output('map-zoom-store', 'data'),
    Input('update-map-btn', 'n_clicks'),
    Input('indicator-selector', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    State('map-center-store', 'data'),
    State('map-zoom-store', 'data')
)
def update_map(n_clicks, indicator, start_date, end_date, center_data, zoom_data):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Get current map center and zoom
    center = [center_data['lat'], center_data['lng']]
    zoom = zoom_data
    
    # Only update center/zoom if the update button was clicked
    if triggered_id == 'update-map-btn':
        # In a real app, you'd get these from the map component
        # For now, we'll just keep the existing values
        pass
    
    m = create_folium_map(center, zoom)
    start_date_str = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date_str = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    
    table_content = None
    merged_data = pd.DataFrame()
    merged_data_effort = pd.DataFrame()
    
    if indicator == "transectos":
        layer = folium.FeatureGroup(name="Transectos com Coral-sol").add_to(m)
        
        locality_data = get_locality_data()
        locality_data['date'] = pd.to_datetime(locality_data['date'], errors='coerce', dayfirst=True)
        filtered_locality_data = locality_data[
            (locality_data['date'] >= pd.to_datetime(start_date_str, errors='coerce')) &
            (locality_data['date'] <= pd.to_datetime(end_date_str, errors='coerce'))
        ]
        
        dafor_data = get_dafor_data()
        dafor_data['date'] = pd.to_datetime(dafor_data['date'], errors='coerce', dayfirst=True)
        dafor_data['dafor_value'] = dafor_data['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        dafor_data = dafor_data.explode('dafor_value')
        dafor_data['dafor_value'] = pd.to_numeric(dafor_data['dafor_value'], errors='coerce')
        
        filtered_dafor_data = dafor_data[
            (dafor_data['date'] >= pd.to_datetime(start_date_str, errors='coerce')) &
            (dafor_data['date'] <= pd.to_datetime(end_date_str, errors='coerce')) &
            (dafor_data['dafor_value'].notna())
        ]
        
        dafor_counts = filtered_dafor_data[filtered_dafor_data['dafor_value'] > 0].groupby('locality_id').size().reset_index(name='dafor_count')
        merged_data = filtered_locality_data.merge(dafor_counts, on='locality_id', how='left').fillna({'dafor_count': 0})
        
        for _, row in merged_data.iterrows():
            try:
                coords_str = row['coords_local']
                try:
                    coords_local = ast.literal_eval(coords_str)
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing coordinates for Locality ID {row['locality_id']}: {e}")
                    continue

                if isinstance(coords_local, list) and len(coords_local) > 0:
                    dafor_count = row['dafor_count']
                    if dafor_count > 30:
                        color = 'red'
                    elif dafor_count > 15:
                        color = 'orange'
                    elif dafor_count > 5:
                        color = 'yellow'    
                    else:
                        color = 'green'

                    folium.PolyLine(
                        coords_local,
                        color=color,
                        popup=folium.Popup(
                            f"<b>Locality:</b> {row['locality_id']}<br>"
                            f"<b>Name:</b> {row['name']}<br>"
                            f"<b>Date:</b> {row['date']}<br>"
                            f"<b>Dafor Count:</b> {dafor_count}",
                            max_width=300
                        ),
                        tooltip=f"Locality {row['locality_id']}"
                    ).add_to(layer)
        
        macro = MacroElement()
        macro._template = Template(legend_transect)
        m.get_root().add_child(macro)
        
        # Prepare table content
        sorted_merged_data = merged_data[['name', 'dafor_count']].sort_values(
            by='dafor_count', ascending=False
        ).rename(columns={'name': 'Localidade', 'dafor_count': 'N. Detecções'})
        sorted_merged_data.index.name = 'id'
        
        table_content = dbc.Card([
            dbc.CardHeader("Número de Transectos com Coral-sol por Localidade"),
            dbc.CardBody([
                dash.dash_table.DataTable(
                    data=sorted_merged_data.reset_index().to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in ['Localidade', 'N. Detecções']],
                    page_size=10,
                    style_table={'overflowX': 'auto'}
                )
            ])
        ])
    
    elif indicator == "esforco":
        layer = folium.FeatureGroup(name="Esforço de Monitoramento").add_to(m)
        
        locality_data = get_locality_data()
        locality_data['date'] = pd.to_datetime(locality_data['date'], errors='coerce', dayfirst=True)
        filtered_locality_data = locality_data[
            (locality_data['date'] >= pd.to_datetime(start_date_str, errors='coerce')) &
            (locality_data['date'] <= pd.to_datetime(end_date_str, errors='coerce'))
        ]
        
        dafor_data = get_dafor_data()
        dafor_data['date'] = pd.to_datetime(dafor_data['date'], errors='coerce', dayfirst=True)
        dafor_data['dafor_value'] = dafor_data['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        dafor_data = dafor_data.explode('dafor_value')
        dafor_data['dafor_value'] = pd.to_numeric(dafor_data['dafor_value'], errors='coerce')
        
        filtered_dafor_data = dafor_data[
            (dafor_data['date'] >= pd.to_datetime(start_date_str, errors='coerce')) &
            (dafor_data['date'] <= pd.to_datetime(end_date_str, errors='coerce')) &
            (dafor_data['dafor_value'].notna())
        ]
        
        dafor_counts_effort = filtered_dafor_data[filtered_dafor_data['dafor_value'] >= 0].groupby('locality_id').size().reset_index(name='dafor_count')
        merged_data_effort = filtered_locality_data.merge(dafor_counts_effort, on='locality_id', how='left').fillna({'dafor_count': 0})
        
        for _, row in merged_data_effort.iterrows():
            try:
                coords_str = row['coords_local']
                try:
                    coords_local = ast.literal_eval(coords_str)
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing coordinates for Locality ID {row['locality_id']}: {e}")
                    continue

                if isinstance(coords_local, list) and len(coords_local) > 0:
                    dafor_count = row['dafor_count']
                    if dafor_count > 10:
                        color = 'red'
                    elif dafor_count > 5:
                        color = 'orange'
                    else:
                        color = 'green'

                    folium.PolyLine(
                        coords_local,
                        color=color,
                        popup=folium.Popup(
                            f"<b>Locality:</b> {row['locality_id']}<br>"
                            f"<b>Name:</b> {row['name']}<br>"
                            f"<b>Date:</b> {row['date']}<br>"
                            f"<b>Dafor Count:</b> {dafor_count}",
                            max_width=300
                        ),
                        tooltip=f"Locality {row['locality_id']}"
                    ).add_to(layer)
        
        macro = MacroElement()
        macro._template = Template(legend_effort)
        m.get_root().add_child(macro)
        
        # Prepare table content
        sorted_merged_data = merged_data_effort[['name', 'dafor_count']].sort_values(
            by='dafor_count', ascending=False
        ).rename(columns={'name': 'Localidade', 'dafor_count': 'Esforço (minutos)'})
        sorted_merged_data.index.name = 'id'
        
        table_content = dbc.Card([
            dbc.CardHeader("Esforço de Monitoramento"),
            dbc.CardBody([
                dash.dash_table.DataTable(
                    data=sorted_merged_data.reset_index().to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in ['Localidade', 'Esforço (minutos)']],
                    page_size=10,
                    style_table={'overflowX': 'auto'}
                )
            ])
        ])
    
    # Save the map to HTML and get the iframe content
    map_html = m.get_root().render()
    
    # Return the map HTML, table content, and current center/zoom
    return map_html, table_content, center_data, zoom_data

@app.callback(
    Output('chart-container', 'children'),
    Input('indicator-selector', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_charts(indicator, start_date, end_date):
    if indicator not in ["detect_ano", "detect_massa"]:
        return None
    
    start_date_str = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date_str = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    
    locality_data = get_locality_data()
    dafor_data = get_dafor_data()
    
    locality_data['date'] = pd.to_datetime(locality_data['date'], errors='coerce', dayfirst=True)
    dafor_data['date'] = pd.to_datetime(dafor_data['date'], errors='coerce', dayfirst=True)
    
    dafor_data['dafor_value'] = dafor_data['dafor_value'].apply(
        lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
    )
    dafor_data = dafor_data.explode('dafor_value')
    dafor_data['dafor_value'] = pd.to_numeric(dafor_data['dafor_value'], errors='coerce')
    
    filtered_dafor_data = dafor_data[
        (dafor_data['date'] >= pd.to_datetime(start_date_str, errors='coerce')) &
        (dafor_data['date'] <= pd.to_datetime(end_date_str, errors='coerce')) &
        (dafor_data['dafor_value'].notna())
    ]
    
    merged_data = locality_data.merge(
        filtered_dafor_data, 
        left_on='locality_id', 
        right_on='locality_id', 
        how='inner'
    )
    
    merged_data['year'] = merged_data['date_y'].dt.year
    
    effort_data = merged_data.groupby(['name', 'year']).agg(
        total_effort=('dafor_value', 'count'),
        total_detections=('dafor_value', lambda x: (x > 0).sum())
    ).reset_index()
    
    effort_data['detections_per_60min'] = (effort_data['total_detections'] / effort_data['total_effort']) * 60
    
    fig = px.line(
        effort_data,
        x='year',
        y='detections_per_60min',
        color='name',
        title='Detecções por 60 minutos de esforço por Ano',
        labels={
            'year': 'Ano',
            'detections_per_60min': 'Detecções por 60 minutos',
            'name': 'Localidade'
        },
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Detecções por 60 minutos de esforço',
        legend_title='Localidade',
        hovermode='x unified',
        yaxis=dict(tickformat=".1f")
    )
    
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Localidade: %{fullData.name}<br>"
            "Detecções: %{customdata[0]}<br>"
            "Esforço: %{customdata[1]} min<br>"
            "Taxa: %{y:.1f} det/60min"
        ),
        customdata=effort_data[['total_detections', 'total_effort']].values
    )
    
    return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)