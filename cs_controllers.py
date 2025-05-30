from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app


from services.data_service import CoralDataService

service = CoralDataService()
localities = service.get_locality_data()
locality_options = [{"label": "Todas", "value": 0}] + sorted(
    [{"label": row["name"], "value": row["locality_id"]} for _, row in localities.iterrows()],
    key=lambda x: x["label"]
)

cs_controls = dbc.Row([
            dcc.Store(id='store-global'),
            html.Img(id="logo", src=app.get_asset_url("logo.png"), style={'width':'100%'}),
            html.H2("Painel de Monitormento do Coral-Sol", style={"margin-top": "30px"}),
            html.H4(
            """Utilize este dashboard para explorar os dados do monitoramento 
            da invasão do coral-sol na REBIO Arvoredo e Entorno. """
            ),
            html.P([
                "Desenvolvido por ",
                html.A("Thiago Silveira", href="https://silveiratcl.github.io/site/", target="_blank"),
            ]),

            html.H3("""Selecione o Período""", style={"margin-top": "30px", "margin-bottom": "20px"}),
            dcc.DatePickerRange(
            id="date-range",
            display_format="DD-MM-YYYY"
        ),
            html.H3("""Selecione a Localidade""", style={"margin-top": "30px", "margin-bottom": "20px"}),
            dcc.Dropdown(
                id="locality-dropdown",
                options=locality_options,
                value=0,
                multi=True,
                placeholder="Selecionar Localidade"
            ),
            html.H3("""Selecione o Indicador""", style={"margin-top": "30px", "margin-bottom": "20px"}),
            dcc.Dropdown(
                id="indicator-dropdown",
                options=[
                    {"label": "DPUE", "value": "dpue"},
                    {"label": "IAR-DAFOR", "value": "dafor"},
                ],
                value="dpue",
                placeholder="Select Indicator"
            ),
            #html.Button("Ver Métodos", id="show-methods-btn", n_clicks=0, style={"margin-top": "20px"}),
            
    ])