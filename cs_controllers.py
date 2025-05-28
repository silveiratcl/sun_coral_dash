from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app


from services.data_service import CoralDataService

service = CoralDataService()
localities = service.get_locality_data()
locality_options = [
    {"label": row["name"], "value": row["locality_id"]}
    for _, row in localities.iterrows()
]



cs_controls = dbc.Row([
            dcc.Store(id='store-global'),
            html.Img(id="logo", src=app.get_asset_url("logo.png"), style={'width':'100%'}),
            html.H3("Painel de Monitormento do Coral-Sol", style={"margin-top": "30px"}),
            html.P(
            """Utilize este dashboard para explorar os dados do monitoramento 
            da invasão do coral-sol na REBIO Arvoredo e Entorno. """
            ),

            html.H3("""Selecione o Período""", style={"margin-top": "30px", "margin-bottom": "20px"}),
            dcc.DatePickerRange(
            id="date-range",
            display_format="DD-MM-YYYY"
        ),
            html.H3("""Selecione a Localidade""", style={"margin-top": "30px", "margin-bottom": "20px"}),
            dcc.Dropdown(
                id="locality-dropdown",
                options=[{"label": "Todas", "value": 0}] + locality_options,
                value=0,
                multi=True,
                placeholder="Selecionar Localidade"
            ),
            html.H3("""Selecione o Indicador""", style={"margin-top": "30px", "margin-bottom": "20px"}),
            dcc.Dropdown(
                id="indicator-dropdown",
                options=[
                    {"label": "DPUE", "value": "dpue"},
                    {"label": "Dias Monit", "value": "dias_monit"},
                    {"label": "Dias Manejo", "value": "dias_manejo"},
                ],
                value="dpue",
                placeholder="Select Indicator"
            )
    ])