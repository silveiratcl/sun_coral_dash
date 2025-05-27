from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from datetime import datetime, date

class DashboardControls:
    def __init__(self):
        # Default values
        self.default_start = date(2020, 1, 1)
        self.default_end = datetime.now().date()
        
    def layout(self):
        return dbc.Card([
            dbc.CardHeader("Dashboard Controls", className="control-header"),
            dbc.CardBody([
                self._temporal_controls(),
                html.Hr(),
                self._locality_controls(),
                html.Hr(),
                self._indicator_controls()
            ])
        ], className="control-card")

    def _temporal_controls(self):
        return html.Div([
            html.H5("Date Range", className="control-title"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Start Date", className="control-label"),
                    dcc.DatePickerSingle(
                        id="date-picker-start",
                        min_date_allowed=date(2010, 1, 1),
                        max_date_allowed=self.default_end,
                        initial_visible_month=self.default_end,
                        date=self.default_start,
                        display_format='YYYY-MM-DD',
                        className="control-datepicker"
                    )
                ], md=6),
                dbc.Col([
                    dbc.Label("End Date", className="control-label"),
                    dcc.DatePickerSingle(
                        id="date-picker-end",
                        min_date_allowed=date(2010, 1, 1),
                        max_date_allowed=self.default_end,
                        initial_visible_month=self.default_end,
                        date=self.default_end,
                        display_format='YYYY-MM-DD',
                        className="control-datepicker"
                    )
                ], md=6)
            ]),
            dbc.Button(
                "Apply Date Range",
                id="date-apply-btn",
                color="primary",
                className="mt-2 control-button"
            ),
            dcc.Store(id='date-range-store')
        ], className="control-section")

    def _locality_controls(self):
        return html.Div([
            html.H5("Location Filter", className="control-title"),
            dbc.Label("Select Localities", className="control-label"),
            dcc.Dropdown(
                id="locality-dropdown",
                options=[
                    {'label': 'All Localities', 'value': 'all'},
                    {'label': 'Recife', 'value': 'recife'},
                    {'label': 'Porto de Galinhas', 'value': 'porto-de-galinhas'}
                ],
                multi=True,
                value=['all'],
                placeholder="Select localities...",
                className="control-dropdown"
            ),
            dcc.Store(id='locality-store')
        ], className="control-section")

    def _indicator_controls(self):
        return html.Div([
            html.H5("DAFOR Indicators", className="control-title"),
            dbc.Label("Select Indicators to Display", className="control-label"),
            dcc.Checklist(
                id="indicator-checklist",
                options=[
                    {'label': ' Abundance', 'value': 'abundance'},
                    {'label': ' Diversity', 'value': 'diversity'},
                    {'label': ' Health Status', 'value': 'health'},
                    {'label': ' Recruitment', 'value': 'recruitment'},
                    {'label': ' Bleaching', 'value': 'bleaching'}
                ],
                value=['abundance'],
                labelClassName="control-checkbox-label",
                className="control-checklist"
            ),
            dcc.Store(id='indicator-store')
        ], className="control-section")

    def register_callbacks(self, app):
        # Date range callback
        @callback(
            Output('date-range-store', 'data'),
            Input('date-apply-btn', 'n_clicks'),
            [State('date-picker-start', 'date'),
             State('date-picker-end', 'date')],
            prevent_initial_call=True
        )
        def update_date_store(n_clicks, start_date, end_date):
            return {
                'start': start_date[:10],
                'end': end_date[:10]
            }

        # Locality selection callback
        @callback(
            Output('locality-store', 'data'),
            Input('locality-dropdown', 'value')
        )
        def update_locality_store(selected):
            return {'selected': selected}

        # Indicator selection callback
        @callback(
            Output('indicator-store', 'data'),
            Input('indicator-checklist', 'value')
        )
        def update_indicator_store(selected):
            return selected