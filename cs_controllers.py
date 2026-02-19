from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app
from services.data_service import CoralDataService

service = CoralDataService()
localities = service.get_locality_data()

# Build name to ID mapping from your data
name_to_id = {row["name"]: row["locality_id"] for _, row in localities.iterrows()}
print("name_to_id:", name_to_id)  # Debug print

# REBIO group (with specified localities removed)
REBIO_LOCALITIES = [
    name_to_id.get("Saco D'água"),
    name_to_id.get("Costão do Saco Dágua"),
    name_to_id.get("Saquinho D'água"),
    name_to_id.get("Ponta do Letreiro"),
    name_to_id.get("Rancho Norte"),
    name_to_id.get("Pedra do Elefante"),
    name_to_id.get("Costa do Elefante"),
    name_to_id.get("Deserta Norte"),
    name_to_id.get("Deserta Sul"),
    name_to_id.get("Costão do Lili"),
    name_to_id.get("Naufrágio do Lili"),
    name_to_id.get("Portinho Norte"),
    name_to_id.get("Portinho Sul"),
    name_to_id.get("Saco da Mulata Norte"),
    name_to_id.get("Saco da Mulata Sul"), 
    name_to_id.get("Toca da Salema"),# missing costao do saco dagua e saquinho dágua
   
]
REBIO_LOCALITIES = [id for id in REBIO_LOCALITIES if id is not None]
print("REBIO_LOCALITIES:", REBIO_LOCALITIES)

# Entorno imediato group (these are the localities you removed from REBIO)
ENTORNO_LOCALITIES = [
    name_to_id.get("Saco do Capim"),  # <-- fixed spelling!
    name_to_id.get("Saco do Batismo"),
    name_to_id.get("Baía das Tartarugas"),
    name_to_id.get("Baía do Engenho"),
    name_to_id.get("Baía do Farol"),
    name_to_id.get("Saco do Vidal"),
     name_to_id.get("Ponta Queimada"),  # Add new locality entorno imediato
]
ENTORNO_LOCALITIES = [id for id in ENTORNO_LOCALITIES if id is not None]
print("ENTORNO_LOCALITIES:", ENTORNO_LOCALITIES)

# REBIO + Entorno Imediato
REBIO_ENTORNO_LOCALITIES = list(set(REBIO_LOCALITIES + ENTORNO_LOCALITIES))
print("REBIO_ENTORNO_LOCALITIES:", REBIO_ENTORNO_LOCALITIES)

GROUP_OPTIONS = [
    {"label": "REBIO + Entorno Imediato", "value": "rebiogrp_entorno"},
    {"label": "REBIO", "value": "rebiogrp"},
    {"label": "Todas", "value": 0},
   
]

locality_options = GROUP_OPTIONS + sorted(
    [{"label": row["name"], "value": row["locality_id"]} for _, row in localities.iterrows()],
    key=lambda x: x["label"]
)

cs_controls = dbc.Row([
    dcc.Store(id='store-global'),
    html.Img(id="logo", src=app.get_asset_url("logo.png"), style={'width':'100%'}),
    html.H2("Painel de Monitoramento do Coral-Sol", style={"margin-top": "30px"}),
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
        value=["rebiogrp_entorno"],
        multi=True,
        placeholder="Selecionar Localidade"
    ),
    html.H3("""Indicadores""", style={"margin-top": "30px", "margin-bottom": "20px"}),
    dcc.Dropdown(
        id="indicator-dropdown",
        options=[
            {"label": "DPUE", "value": "dpue"},
            {"label": "IAR-DAFOR", "value": "dafor"},
            {"label": "OCORRÊNCIAS", "value": "occurrences"},
            {"label": "MASSA MANEJADA (KG)", "value": "management"},
            {"label": "ÚLTIMO MANEJO (DIAS)", "value": "days_since_management"},
            {"label": "ÚLTIMO MONITORAMENTO (DIAS)", "value": "days_since_monitoring"},
            {"label": "NÚMERO DE MONITORAMENTOS", "value": "monitoring_intensity"},
        ],
        value="dpue",
        placeholder="Select Indicator"
    ),
])

def filter_localities(selected_localities, df):
    if selected_localities is None or 0 in selected_localities:
        return df

    ids = []
    for loc in selected_localities:
        if loc == "rebiogrp":
            ids.extend(REBIO_LOCALITIES)
        elif loc == "rebiogrp_entorno":
            ids.extend(REBIO_ENTORNO_LOCALITIES)
        else:
            try:
                ids.append(int(loc))
            except Exception:
                pass
    ids = list(set(ids))
    #print("Filtering with IDs:", ids)  # Debug print
    filtered = df[df["locality_id"].isin(ids)]
    #print("Filtered rows:", len(filtered))  # Debug print
    return filtered