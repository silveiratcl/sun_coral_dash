from dash import html

methods_layout = html.Div([
    html.H2("Métodos Utilizados no Dashboard"),
    html.P("""
        Este painel utiliza os seguintes métodos para processar e visualizar os dados:
    """),
    html.Ul([
        html.Li([
            html.B("get_locality_data(): "),
            "Busca e processa os dados das localidades, extraindo coordenadas geográficas."
        ]),
        html.Li([
            html.B("get_dafor_data(start_date, end_date): "),
            "Busca os dados de abundância (DAFOR) e filtra pelo período selecionado."
        ]),
        html.Li([
            html.B("calculate_locality_length(coords_local): "),
            "Calcula o comprimento de cada localidade com base nas coordenadas."
        ]),
        html.Li([
            html.B("get_dpue_by_locality(start_date, end_date): "),
            "Processa os dados para calcular o DPUE (Detecções por Unidade de Esforço) por localidade."
        ]),
        html.Li([
            html.B("Visualizações: "),
            "Os gráficos de mapa e histograma são gerados com Plotly, utilizando as métricas calculadas."
        ]),
    ]),
    html.Img(src="/assets/methods_example.png", style={"width": "60%", "margin": "30px 0"}),  # Add your image to assets/
    html.Button("Voltar", id="back-to-dashboard-btn", n_clicks=0, style={"margin-top": "30px"}),
])