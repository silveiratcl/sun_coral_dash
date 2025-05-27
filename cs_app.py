from controllers import DashboardControls

# Initialize controls
controls = DashboardControls()

app.layout = dbc.Container([
    dbc.Row([
        # Controls column (25% width)
        dbc.Col([
            controls.layout()
        ], md=3, style={
            "padding": "20px",
            "background": "#f8f9fa",
            "height": "100vh"
        }),
        
        # Visualizations column (75% width)
        dbc.Col([
            html.Div(id="map-container"),
            html.Div(id="charts-container")
        ], md=9)
    ])
], fluid=True)

# Register all callbacks
controls.register_callbacks(app)