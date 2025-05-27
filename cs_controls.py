from dash import dcc, html
import dash_bootstrap_components as dbc
from services.data_services import CoralDataService

# Get real localities for dropdown
data_service = CoralDataService()
localities = data_service._get_locality_data()

controls = dbc.Card([
    html.H5("Filters", className="card-header"),
    dbc.CardBody([
        html.Label("Date Range"),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date='2020-01-01',
            end_date='2023-12-31',
            display_format='YYYY-MM-DD'
        ),
        html.Label("Locality", className="mt-3"),
        dcc.Dropdown(
            id='locality-dropdown',
            options=[{'label': 'All', 'value': 'all'}] + [
                {'label': row['name'], 'value': row['locality_id']}
                for _, row in localities.iterrows()
            ],
            value=['all'],
            multi=True
        )
    ])
])