import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True  # <-- Add this line
)
#server = app.server
app.scripts.config.serve_locally = True
app.title = "Coral-Sol Dashboard"