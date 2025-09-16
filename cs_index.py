import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
from cs_map import (
    build_dafor_sum_map_figure,
    build_map_figure,
    build_occurrence_map_figure,
    build_management_map_figure,
    build_days_since_management_map_figure,
    build_days_since_monitoring_map_figure,  
)    

from cs_controllers import cs_controls, REBIO_LOCALITIES, REBIO_ENTORNO_LOCALITIES
from services.data_service import CoralDataService
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from cs_map import build_map_figure
from cs_histogram import (
    build_histogram_figure,
    build_locality_bar_figure, 
    build_dafor_histogram_figure,
    build_dafor_sum_bar_figure,
    build_accumulated_mass_year_figure,
    build_days_since_management_bar_figure,  
    build_days_since_monitoring_bar_figure,
    build_removal_ratio_year_figure
) 
from cs_tables import build_occurrences_table
from cs_methods import methods_layout  # Your text tab layout
from services.data_service import CoralDataService
#from cs_methods import methods_layout
from dash import ctx
import plotly.graph_objects as go
from dash.dependencies import Output, State
from dash import callback, no_update
from flask import send_from_directory, Flask, Response
import sqlalchemy
import os
import base64
import requests
import pandas as pd  # <-- Import pandas

# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           title="Coral-Sol Dashboard" )
server = app.server

# Define dashboard_layout 
dashboard_layout = html.Div([
    html.Div(dcc.Loading(dcc.Graph(id="cs-map-graph", config={'scrollZoom': True}), type="circle"), id="div-map"),
    html.Div(dcc.Loading(dcc.Graph(id="cs-histogram-graph"), type="circle"), id="div-hist"),
    html.Div(dcc.Loading(dcc.Graph(id="cs-locality-bar-graph"), type="circle"), id="div-bar"),
    html.Div(dcc.Loading(dcc.Graph(id="cs-dafor-histogram-graph"), type="circle"), id="div-dafor-hist"),
    html.Div(dcc.Loading(dcc.Graph(id="cs-dafor-sum-bar-graph"), type="circle"), id="div-dafor-sum-bar"),
    html.Div(dcc.Loading(dcc.Graph(id="cs-line-graph"), type="circle"), id="div-line"),
    html.Div(dcc.Loading(dcc.Graph(id="cs-removal-ratio-graph"), type="circle"), id="div-removal-ratio"),
    html.Div(id="occurrences-table-container"),
])

# Define the modal for displaying occurrence details
modal = dbc.Modal(
    [
        dbc.ModalHeader("Detalhes da Ocorrência"),
        dbc.ModalBody(id="modal-body"),
        dbc.ModalFooter(
            dbc.Button("Fechar", id="close-modal", className="ml-auto")
        ),
    ],
    id="modal",
    is_open=False,
)




app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                cs_controls,
                #metrics_widgets,  # <-- Add this line
            ], md=3, style={
                "padding-right": "25px",
                "padding-left": "25px",
                "padding-top": "50px"
            }),
            dbc.Col([
                dcc.Tabs(
    id="main-tabs",
    value="dashboard",  # default tab
    children=[
        dcc.Tab(label='Dashboard', value="dashboard", children=[dashboard_layout]),
        dcc.Tab(label='Métodos e Texto', value="methods", children=[methods_layout]),
    ]
)
            ], md=9),
            
        ]),
        modal # <--  modal here, outside the Row so it overlays the whole page
    ],
    fluid=True,
)


#=========================================
# Callbacks

# Update map and histogram based on user input
@app.callback(
    [
        Output("cs-map-graph", "figure"),
        Output("cs-histogram-graph", "figure"),
        Output("cs-locality-bar-graph", "figure"),
        Output("cs-dafor-histogram-graph", "figure"),
        Output("cs-dafor-sum-bar-graph", "figure"),
        Output("cs-line-graph", "figure"),
        Output("cs-removal-ratio-graph", "figure"),
        Output("div-hist", "style"),
        Output("div-bar", "style"),
        Output("div-dafor-hist", "style"),
        Output("div-dafor-sum-bar", "style"),
        Output("div-line", "style"),
        Output("div-removal-ratio", "style"),  
        Output("occurrences-table-container", "children"),
    ],
    [
        Input("indicator-dropdown", "value"),
        Input("locality-dropdown", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ]
)

def update_visuals(indicator, selected_localities, start_date, end_date):
    service = CoralDataService()

    # Normalize selected_localities to handle group selection
    if not selected_localities or 0 in (selected_localities if isinstance(selected_localities, list) else [selected_localities]):
        selected_localities = None
    else:
        ids = []
        for loc in selected_localities if isinstance(selected_localities, list) else [selected_localities]:
            if loc == "rebiogrp":
                ids.extend(REBIO_LOCALITIES)
            elif loc == "rebiogrp_entorno":
                ids.extend(REBIO_ENTORNO_LOCALITIES)
            else:
                try:
                    ids.append(int(loc))
                except Exception:
                    pass
        selected_localities = list(set(ids)) if ids else None

    # Default empty figures
    fig_map = go.Figure()
    fig_hist = go.Figure()
    fig_bar = go.Figure()
    fig_dafor_hist = go.Figure()
    fig_dafor_sum_bar = go.Figure()
    fig_line = go.Figure()
    fig_removal_ratio = go.Figure()  

    # Default: show all
    style_hide = {'display': 'none'}
    style_show = {'display': 'block'}

    # Default styles for charts
    hist_style = bar_style = dafor_hist_style = dafor_sum_bar_style = style_hide
    line_style = style_hide
   
    occurrences_table = None  # <--- Add this line

    if indicator == "dpue":
        dpue_df = service.get_dpue_by_locality(start_date, end_date)
        if selected_localities:
            dpue_df = dpue_df[dpue_df['locality_id'].isin(selected_localities)]
        fig_map = build_map_figure(dpue_df)
        fig_hist = build_histogram_figure(dpue_df)
        fig_bar = build_locality_bar_figure(dpue_df)
        # DAFOR charts remain empty
        hist_style = style_show
        bar_style = style_show
        dafor_hist_style = style_hide
        dafor_sum_bar_style = style_hide
        removal_ratio_style = style_hide
        

    elif indicator == "dafor":
        # Get DAFOR sum per locality (for bar and map)
        df_dafor_sum = service.get_sum_of_dafor_by_locality(start_date, end_date)
        if selected_localities:
            df_dafor_sum = df_dafor_sum[df_dafor_sum['locality_id'].isin(selected_localities)]
        fig_map = build_dafor_sum_map_figure(df_dafor_sum)

        # Get all DAFOR values (for histogram)
        dafor_df = service.get_dafor_data(start_date, end_date)
        if selected_localities:
            dafor_df = dafor_df[dafor_df['locality_id'].isin(selected_localities)]
        # If dafor_value is a string of comma-separated values, flatten it:
        if dafor_df['dafor_value'].apply(lambda x: isinstance(x, str) and ',' in x).any():
            dafor_df['dafor_value'] = dafor_df['dafor_value'].apply(
                lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
            )
            dafor_values = pd.Series([v for sublist in dafor_df['dafor_value'] for v in sublist])
        else:
            dafor_values = pd.to_numeric(dafor_df['dafor_value'], errors='coerce')
        dafor_values = dafor_values.dropna()
        dafor_values = dafor_values[(dafor_values >= 0) & (dafor_values <= 10)]

        fig_dafor_hist = build_dafor_histogram_figure(dafor_values)
        fig_dafor_sum_bar = build_dafor_sum_bar_figure(df_dafor_sum)
        # DPUE charts remain empty
        hist_style = style_hide
        bar_style = style_hide
        dafor_hist_style = style_show
        dafor_sum_bar_style = style_show
        removal_ratio_style = style_hide

    elif indicator == "occurrences":
        occurrences_df = service.get_occurrences_data(start_date, end_date)
        # Keep a copy for the map (needs spot_coords)
        map_df = occurrences_df.copy()

        # Select and rename columns for display in the table
        columns_to_show = [
            "date", "name", "depth", "access", "geomorphology"
        ]
        table_df = occurrences_df[columns_to_show].rename(columns={
            "date": "Data",
            "name": "Localidade",
            "depth": "Profundidade",
            "access": "Acesso",
            "geomorphology": "Geomorfologia"
        })

        fig_map = build_occurrence_map_figure(map_df)
        occurrences_table = build_occurrences_table(table_df)
        # Hide other charts
        fig_hist = go.Figure()
        fig_bar = go.Figure()
        fig_dafor_hist = go.Figure()
        fig_dafor_sum_bar = go.Figure()
        hist_style = bar_style = dafor_hist_style = dafor_sum_bar_style = style_hide
        removal_ratio_style = style_hide

    elif indicator == "management":
        df_management = service.get_management_data(start_date, end_date)
        localities = service.get_locality_data()[['locality_id', 'name']]
        localities.columns = localities.columns.str.lower()
        df_management.columns = df_management.columns.str.lower()
        df_management = df_management.merge(localities, on='locality_id', how='left')
        df_management['year'] = pd.to_datetime(df_management['date']).dt.year

        fig_map = build_management_map_figure(df_management)
        fig_line = build_accumulated_mass_year_figure(df_management)
        fig_removal_ratio = build_removal_ratio_year_figure(df_management)  # <-- Add this line
        line_style = style_show
        hist_style = bar_style = dafor_hist_style = dafor_sum_bar_style = style_hide
        removal_ratio_style = style_show

    elif indicator == "days_since_management":
        df_days_since = service.get_days_since_last_management(start_date, end_date)
        # debug print
        print("DataFrame for chart:", df_days_since.head())
        print("Rows for chart:", len(df_days_since))
        if selected_localities:
            df_days_since = df_days_since[df_days_since['locality_id'].isin(selected_localities)]
        fig_map = build_days_since_management_map_figure(df_days_since)
        fig_bar = build_days_since_management_bar_figure(df_days_since)
        # Hide other charts, show map and bar
        fig_hist = go.Figure()
        fig_dafor_hist = go.Figure()
        fig_dafor_sum_bar = go.Figure()
        fig_line = go.Figure()
        hist_style = style_hide
        bar_style = style_show
        dafor_hist_style = style_hide
        dafor_sum_bar_style = style_hide
        removal_ratio_style = style_hide
   
    elif indicator == "days_since_monitoring":
        df_days_since = service.get_days_since_last_monitoring(start_date, end_date)
        # debug print
        #print("DataFrame for chart:", df_days_since.head())
        #print("Rows for chart:", len(df_days_since))
        print("All locality_ids in data:", df_days_since["locality_id"].unique())
        if selected_localities:
            df_days_since = df_days_since[df_days_since['locality_id'].isin(selected_localities)]
            print("Selected localities:", selected_localities)
            print("Filtered locality_ids:", df_days_since["locality_id"].unique())
            print("Filtered rows:", len(df_days_since))
        fig_map = build_days_since_monitoring_map_figure(df_days_since)
        fig_bar = build_days_since_monitoring_bar_figure(df_days_since)  # <-- bar plot below map
        fig_hist = go.Figure()
        fig_dafor_hist = go.Figure()
        fig_dafor_sum_bar = go.Figure()
        fig_line = go.Figure()
        hist_style = style_hide
        bar_style = style_show
        dafor_hist_style = style_hide
        dafor_sum_bar_style = style_hide
        removal_ratio_style = style_hide
    else:
        hist_style = bar_style = dafor_hist_style = dafor_sum_bar_style = style_hide

    return (
        fig_map, fig_hist, fig_bar, fig_dafor_hist, fig_dafor_sum_bar, fig_line, fig_removal_ratio,
        hist_style, bar_style, dafor_hist_style, dafor_sum_bar_style, line_style, removal_ratio_style,
        occurrences_table
    )
    



@app.callback(
    [Output("modal", "is_open"), Output("modal-body", "children")],
    [Input("cs-map-graph", "clickData"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")],
)

def display_modal(clickData, n_close, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, no_update

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger == "cs-map-graph" and clickData:
        point = clickData["points"][0]
        lat = point["lat"]
        lon = point["lon"]
        customdata = point.get("customdata", ["", ""])
        sub_img_url = customdata[0]
        sup_img_url = customdata[1]

        # Fetch base64 from API
        def fetch_base64(url):
            if not url:
                return None
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    return resp.text
            except Exception as e:
                print(f"Error fetching image: {e}")
            return None

        sub_img_b64 = fetch_base64(sub_img_url)
        sup_img_b64 = fetch_base64(sup_img_url)

        body = html.Div([
            html.P(f"Latitude: {lat}, Longitude: {lon}"),
            html.Img(src=f"data:image/jpeg;base64,{sub_img_b64}", style={"width": "100%", "margin-bottom": "10px"}) if sub_img_b64 else html.P("Sem foto subaquática"),
            html.Br(),
            html.Img(src=f"data:image/jpeg;base64,{sup_img_b64}", style={"width": "100%"}) if sup_img_b64 else html.P("Sem foto de superfície"),
        ])
        return True, body

    if trigger == "close-modal" and is_open:
        return False, no_update

    return is_open, no_update

# Define your metrics layout here
metrics_layout = dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardHeader("Massa Manejada (kg)"),
        dbc.CardBody(html.H4(id="total-mass-managed", children="0"))
    ], color="primary", inverse=True), md=4),
    dbc.Col(dbc.Card([
        dbc.CardHeader("Ações de Manejo"),
        dbc.CardBody(html.H4(id="num-management-actions", children="0"))
    ], color="info", inverse=True), md=4),
    dbc.Col(dbc.Card([
        dbc.CardHeader("Km Monitorados"),
        dbc.CardBody(html.H4(id="km-monitored", children="0"))
    ], color="secondary", inverse=True), md=4),
], className="mb-4")

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                cs_controls,
                metrics_layout,  # <-- Add this line
            ], md=3, style={
                "padding-right": "25px",
                "padding-left": "25px",
                "padding-top": "50px"
            }),
            dbc.Col([
                dcc.Tabs(
    id="main-tabs",
    value="dashboard",  # default tab
    children=[
        dcc.Tab(label='Dashboard', value="dashboard", children=[dashboard_layout]),
        dcc.Tab(label='Sobre', value="methods", children=[methods_layout]),
    ]
)
            ], md=9),
            
        ]),
        modal,  # <--  modal here, outside the Row so it overlays the whole page
    ],
    fluid=True,
)

@app.callback(
    [
        Output("total-mass-managed", "children"),
        Output("num-management-actions", "children"),
        Output("km-monitored", "children"),
    ],
    [
        Input("indicator-dropdown", "value"),
        Input("locality-dropdown", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ]
)
def update_metrics(indicator, selected_localities, start_date, end_date):
    service = CoralDataService()
    # Replace with your real data logic:
    df_management = service.get_management_data(start_date, end_date)
    total_mass = df_management["managed_mass_kg"].sum()
    num_actions = len(df_management)
    # Example: if you have a column 'km_monitored'
    km_monitored = service.get_km_monitored(start_date, end_date)

    return f"{total_mass:,.0f}", f"{num_actions:,}", f"{km_monitored:,.2f}"

from dash.dependencies import Input, Output

@app.callback(
    Output("main-tabs", "value"),
    Input("back-to-dashboard-btn", "n_clicks"),
    prevent_initial_call=True
)
def go_back_to_dashboard(n_clicks):
    if n_clicks:
        return "dashboard"
    return dash.no_update

if __name__ == "__main__":
    app.run(debug=True)


