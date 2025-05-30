from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
from cs_map import build_dafor_sum_map_figure, build_map_figure
from cs_controllers import cs_controls
from services.data_service import CoralDataService
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from cs_map import build_map_figure
from cs_histogram import (
    build_histogram_figure,
    build_locality_bar_figure, 
    build_dafor_histogram_figure,
    build_dafor_sum_bar_figure
)

from services.data_service import CoralDataService
#from cs_methods import methods_layout
from dash import ctx
import plotly.graph_objects as go
from dash.dependencies import Output


# Define dashboard_layout 
dashboard_layout = html.Div([
    html.Div(dcc.Graph(id="cs-map-graph", config={'scrollZoom': True}), id="div-map"),
    html.Div(dcc.Graph(id="cs-histogram-graph"), id="div-hist"),
    html.Div(dcc.Graph(id="cs-locality-bar-graph"), id="div-bar"),
    html.Div(dcc.Graph(id="cs-dafor-histogram-graph"), id="div-dafor-hist"),
    html.Div(dcc.Graph(id="cs-dafor-sum-bar-graph"), id="div-dafor-sum-bar"),
])



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([cs_controls], md=3, style={
                "padding-right": "25px",
                "padding-left": "25px",
                "padding-top": "50px"
            }),
            dbc.Col([
                dashboard_layout
            ], md=9),
        ])
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
        Output("div-hist", "style"),
        Output("div-bar", "style"),
        Output("div-dafor-hist", "style"),
        Output("div-dafor-sum-bar", "style"),
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

    # Normalize selected_localities
    if not selected_localities or 0 in (selected_localities if isinstance(selected_localities, list) else [selected_localities]):
        selected_localities = None
    elif isinstance(selected_localities, int):
        selected_localities = [selected_localities]

    # Default empty figures
    fig_map = go.Figure()
    fig_hist = go.Figure()
    fig_bar = go.Figure()
    fig_dafor_hist = go.Figure()
    fig_dafor_sum_bar = go.Figure()

    # Default: show all
    style_show = {}
    style_hide = {"display": "none"}

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

    elif indicator == "dafor":
        df_dafor_sum = service.get_sum_of_dafor_by_locality(start_date, end_date)
        if selected_localities:
            df_dafor_sum = df_dafor_sum[df_dafor_sum['locality_id'].isin(selected_localities)]
        fig_map = build_dafor_sum_map_figure(df_dafor_sum)
        dafor_values = service.get_dafor_value_histogram_data(start_date, end_date)
        fig_dafor_hist = build_dafor_histogram_figure(dafor_values)
        fig_dafor_sum_bar = build_dafor_sum_bar_figure(df_dafor_sum)
        # DPUE charts remain empty
        hist_style = style_hide
        bar_style = style_hide
        dafor_hist_style = style_show
        dafor_sum_bar_style = style_show

    else:
        hist_style = bar_style = dafor_hist_style = dafor_sum_bar_style = style_hide

    return (
        fig_map, fig_hist, fig_bar, fig_dafor_hist, fig_dafor_sum_bar,
        hist_style, bar_style, dafor_hist_style, dafor_sum_bar_style
    )

if __name__ == "__main__":
    app.run(debug=True)


