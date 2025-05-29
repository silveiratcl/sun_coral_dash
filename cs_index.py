from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from cs_map import build_map_figure
from cs_histogram import build_histogram_figure
from cs_controllers import cs_controls
from services.data_service import CoralDataService
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from cs_map import build_map_figure
from cs_histogram import build_histogram_figure, build_locality_bar_figure
from cs_controllers import cs_controls
from services.data_service import CoralDataService
from cs_methods import methods_layout
from dash import ctx
import plotly.graph_objects as go


# Define dashboard_layout 
dashboard_layout = html.Div([
    dcc.Graph(id="cs-map-graph", config={'scrollZoom': True}),
    dcc.Graph(id="cs-histogram-graph"),
    dcc.Graph(id="cs-locality-bar-graph"),
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
         Output("cs-locality-bar-graph", "figure"),  # New output
    ],
    [
        Input("locality-dropdown", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ]
)
def update_visuals(selected_localities, start_date, end_date):
    # Normalize selected_localities
    if not selected_localities or 0 in (selected_localities if isinstance(selected_localities, list) else [selected_localities]):
        selected_localities = None
    elif isinstance(selected_localities, int):
        selected_localities = [selected_localities]

    service = CoralDataService()
    dpue_df = service.get_dpue_by_locality(start_date, end_date)

    # Filter by locality if needed
    if selected_localities:
        dpue_df = dpue_df[dpue_df['locality_id'].isin(selected_localities)]

    # Always build the map (should handle empty or missing data internally)
    fig_map = build_map_figure(selected_localities)

    # For histogram and bar: show empty dark figures if no data
    if dpue_df.empty or dpue_df["DPUE"].dropna().empty:
        empty_hist = go.Figure()
        empty_hist.update_layout(
            template="plotly_dark",
            xaxis_title="DPUE",
            yaxis_title="Contagem",
            bargap=0.1,
            margin={"r":10,"t":20,"l":10,"b":40},
            height=180
        )
        empty_bar = go.Figure()
        empty_bar.update_layout(
            template="plotly_dark",
            xaxis_title="DPUE",
            yaxis_title="Localidade",
            margin={"r":10,"t":20,"l":10,"b":40},
            height=300
        )
        return fig_map, empty_hist, empty_bar

    fig_hist = build_histogram_figure(dpue_df)
    fig_bar = build_locality_bar_figure(dpue_df)
    return fig_map, fig_hist, fig_bar

if __name__ == "__main__":
    app.run(debug=True)


