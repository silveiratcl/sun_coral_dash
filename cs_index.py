from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from cs_map import build_map_figure
from cs_histogram import build_histogram_figure
from cs_controllers import cs_controls
from services.data_service import CoralDataService

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
                dcc.Graph(id="cs-map-graph", config={'scrollZoom': True}),
                dcc.Graph(id="cs-histogram-graph"),
            ], md=9),
        ])
    ],
    fluid=True,
)

@app.callback(
    [Output("cs-map-graph", "figure"),
     Output("cs-histogram-graph", "figure")],
    [Input("locality-dropdown", "value")]
)
def update_visuals(selected_localities):
    # Normalize selected_localities
    if not selected_localities or 0 in (selected_localities if isinstance(selected_localities, list) else [selected_localities]):
        selected_localities = None
    elif isinstance(selected_localities, int):
        selected_localities = [selected_localities]

    # Build map
    fig_map = build_map_figure(selected_localities)

    # Build histogram (filter DPUE data if needed)
    service = CoralDataService()
    dpue_df = service.get_dpue_by_locality()
    if selected_localities:
        dpue_df = dpue_df[dpue_df['locality_id'].isin(selected_localities)]
    fig_hist = build_histogram_figure(dpue_df)

    return fig_map, fig_hist

if __name__ == "__main__":
    app.run(debug=True)