from dash import html

methods_layout = html.Div([
    html.Img(src="assets/img/head_sobre.png", 
             style={"width": "80%", 
                    "margin": "30px auto", 
                    "display": "block",
                    "border-radius": "20px"}),
    html.Br(),                
    html.Br(),

    html.H1("Dashboard dos dados Monitoramento e Manejo de coral-sol"), 
    html.Br(),
    html.Br(),
    html.P("""
            Um dashboard é uma ferramenta incrivelmente valiosa que permite aos usuários visualizar e compreender dados complexos de forma simples.
            Ao atuar como uma centralização de dados processados, ele apresenta uma riqueza de métricas essenciais, tendências em um formato visualmente
            atraente e intuitivo. Isso o torna uma solução ideal para agências ambientais que buscam adquirir recursos valiosos para a Detecção Precoce -   
           Resposta Rápida (EDRR) de espécies invasoras. Nesta documentação, exploraremos os componentes fundamentais da interpretação de dados no 
           Dashboard de Monitoramento do Coral-Sol - PACS REBIO Arvoredo.
    """),
    html.Br(), 
    html.Br(),
    
    html.H1("Protocolo de Monitoramento"),
    html.Br(),
    html.H2("""
        Aquisição das informações em campo
    """),
    html.Br(),
    html.P("""
        Os dados de monitoramento são obtidos em localidades, onde é definido um segmento, 
        e na extensão de um segmento são coletadas informações relacionadas a transectos a cada minuto.
    """),
    html.Br(),

    html.Img(src="assets/img/segmento.png", 
             style={"width": "50%", 
                    "margin": "30px auto", 
                    "display": "block", 
                    "border-radius": "20px"}),  

    html.Br(),
    html.Br(),
    html.H1("Busca Ativa"),
    html.Br(),
    html.H2("""
        Snorkeling
    """),

    html.P("""
            Na faixa de profundidade de zero a 2 metros do segmento de amostragem, o monitoramento será realizado por um mergulhador de snorkeling. 
            O mergulhador buscará dentro dessa faixa de profundidade, cobrindo o segmento de amostragem e procurando possíveis ocorrências de coral-sol.
    """),
    html.Br(),
     html.H2("""
        Mergulho Autônomo (SCUBA)
    """),
    html.P("""
        As amostras de mergulho autônomo serão conduzidas por dois pares de mergulhadores. A área operacional para cada par será determinada 
           por faixas de profundidade (por exemplo, de 0 a 8m e de 9 a 15m) ao longo da costa rochosa, visando cobrir a maior extensão vertical 
           possível. A divisão das profundidades de varredura entre os pares pode variar dependendo das características batimétricas de cada segmento de amostragem.
    """),
    html.Br(),
    html.Br(),

    html.Img(src="assets/img/monitora_dash.png", 
             style={"width": "50%", 
                    "margin": "30px auto", 
                    "display": "block", 
                    "border-radius": "20px"}),  
    html.Br(),
    html.Br(),

    html.H1("DAFOR"),
    html.Br(),
    html.Br(),

    html.P("""
           Para classificar os níveis de invasão nos segmentos amostrados, utilizamos uma escala semi-quantitativa de abundância 
           conhecida como escala DAFOR (Sutherland, 2006), especificamente adaptada para avaliar a abundância de coral-sol (Creed & Fleury, 2009). 
           A escala atribui valores a cada classe de abundância relativa, que são descritas da seguinte forma:
           """),
    html.Br(),
    html.Ul([
        html.Li([
            html.B("Dominante:"),
            "Esta categoria representa populações altamente evidentes que formam predominantemente manchas monoespecíficas de pelo menos 1m². Essas manchas contêm numerosas colônias isoladas e/ou manchas menores espalhadas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.B("Abundante: "),
            "Os agrupamentos nesta categoria formam manchas essencialmente monoespecíficas variando de 50 a 100 cm de diâmetro. Semelhante à categoria dominante, colônias isoladas e/ou pequenas manchas espalhadas podem ser observadas ao longo do substrato."
        ]),
        html.Br(),
        html.Li([
            html.B("Frequente: "),
            "Esta classe inclui colônias isoladas e/ou pequenas manchas variando de 10 a 50 cm de diâmetro, espalhadas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.B("Ocasional: "),
            "Esta categoria abrange casos em que entre 1 e 5 colônias estão dispersas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.B("Raro: "),
            "Esta categoria abrange casos em que entre 1 e 5 colônias estão dispersas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.B("Ausente: "),
            "Sem registro de coral-sol no minuto amostrado."
        ]),
    ]),
    html.Br(),
    html.Br(),

    html.H1("Índice de Abundância Relativa"),
    html.Br(),

    html.P("""
            As observações feitas na escala DAFOR são então convertidas para um índice de abundância relativa (RAI) usando a seguinte classificação: 
           10 - dominante, 8 - abundante, 6 - frequente, 4 - ocasional, 2 - raro; zero - ausente. A ilustração abaixo ilustra as categorias da escala DAFOR
              e seus respectivos valores de RAI.
        
           """),
    html.Br(),
    html.Img(src="assets/img/dafor_eng.png", 
             style={"width": "50%", 
                    "margin": "30px auto", 
                    "display": "block", 
                    "border-radius": "20px"}), 
    html.Br(),
    html.Br(),
    html.H1("Indicadores - em construção"),
    html.P("Esta seção está em construção e será atualizada em breve."),
    html.Br(),
    html.Br(),
                    





    html.H1("Referências e Links úteis"),
    html.Br(),
    html.Br(),

    html.Ul([
        html.Li("CREED, et al. 2025. A bioinvasão do Coral-Sol. in press"),
        html.Li("CREED, J.C.; FLEURY, B.G. 2009. Monitoramento extensivo de coral-sol (Tubastraea coccinea e T. tagusensis): protocolo de semi-quantificação. Projeto Coral-Sol, Instituto Biodiversidade Marinha, Rio de Janeiro. p 1."),
        html.Li("CREED JC; JUNQUEIRA ADOR, FLEURY BG, MANTELLATO MC, OIGMAN-PSZCZOL SS. 2017. The Sun-Coral Project: the first social-environmental initiative to manage the biological invasion of Tubastraea spp. in Brazil. Management of Biological Invasions 8(2): 181."),
        html.Li("CREED JC, FENNER D, SAMMARCO P, CAIRNS S, CAPEL K., JUNQUEIRA AO, CRUZ I, MIRANDA RJ, CARLOS-JUNIORL, MANTELLATO MC, OIGMAN-PSZCZOL, S. 2017. The invasion of the azooxanthellate coral Tubastraea (Scleractinia: Dendrophylliidae) throughout the world: history, pathways and vectors. Biological Invasions 19: 283-305."),
        html.Li("SCRISP, DJ; SOUTHWARD, AJ. 1958. The distribution of intertidal organisms along the coasts of the English Channel. Journal of the Marine Biological Association UK 37: 157-208."),
        html.Li("GRAINGER, S.; MAO, F.; BUYTAERT, W. 2016. Environmental data visualisation for non-scientific contexts: Literature review and design framework. Environmental Modelling & Software, 85, 299-318."),
        html.Li("SILVEIRA, T.C.L.; CARVALHAL, A.; SEGAL, B. 2023. Protocolo Técnico de monitoramento de coral-sol na REBIO Arvoredo e entorno. In: Protocolos Técnicos de Campo. PACS Arvoredo. Projeto PACS Arvoredo. Florianópolis, 56 p."),
        html.Li("SUTHERLAND, W.J. 2006. Ecological Census Techniques: A Handbook. 2nd edition. Cambridge University Press, Cambridge, UK."),
    ]),






    html.Button("Voltar", id="back-to-dashboard-btn", n_clicks=0, style={"margin-top": "30px"}),
])