from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    return html.Div(
        [
            html.H4("Map Layers", className="text-center mb-4"),
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dcc.Checklist(
                                id='localidade-toggle',
                                options=[{'label': 'Show Localidades', 'value': 'show'}],
                                value=['show']
                            ),
                            dcc.Checklist(
                                id='dafor-toggle',
                                options=[{'label': 'Show DAFOR', 'value': 'show'}],
                                value=[]
                            ),
                            dcc.Checklist(
                                id='ocorrencias-toggle',
                                options=[{'label': 'Show Ocorrências', 'value': 'show'}],
                                value=[]
                            ),
                            dcc.Checklist(
                                id='manejo-toggle',
                                options=[{'label': 'Show Manejo', 'value': 'show'}],
                                value=[]
                            ),
                        ],
                        title="Data Layers"
                    ),
                    dbc.AccordionItem(
                        [
                            dcc.DatePickerRange(
                                id='date-range',
                                min_date_allowed='2010-01-01',
                                max_date_allowed='2025-12-31',
                                start_date='2020-01-01',
                                end_date='2023-12-31'
                            )
                        ],
                        title="Date Filter"
                    ),
                ],
                start_collapsed=True,
                className="mb-3"
            )
        ],
        className="bg-light p-3",
        style={
            'height': '100vh',
            'position': 'fixed',
            'width': '250px'
        }
    )