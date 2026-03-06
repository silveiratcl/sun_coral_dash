"""Simple test to verify tabs are working"""
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Tab Test"),
    dcc.Tabs(
        id="test-tabs",
        value="tab1",
        children=[
            dcc.Tab(label='Tab 1', value="tab1", children=[html.Div("Content 1")]),
            dcc.Tab(label='Tab 2', value="tab2", children=[html.Div("Content 2")]),
            dcc.Tab(label='Tab 3', value="tab3", children=[html.Div("Content 3")]),
        ]
    )
])

if __name__ == '__main__':
    print("Test app running at http://127.0.0.1:8051")
    app.run_server(debug=True, port=8051)
