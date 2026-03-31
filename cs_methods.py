from dash import html

methods_layout = html.Div([
    html.Img(src="assets/img/head_sobre.png",
             style={"width": "80%",
                    "margin": "30px auto",
                    "display": "block",
                    "border-radius": "20px"}),
    html.Br(),
    html.Br(),

    html.H1("DADOS DO MONITORAMENTO E MANEJO DO CORAL-SOL - REBIO ARVOREDO",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #2a7ae2",
    "paddingBottom": "5px"
    }),
    html.Br(),
    html.Br(),
    html.H3("""
            Um dashboard de dados é uma ferramenta que visa ajudar usuários/gestores a visualizar e compreender dados complexos.
            Ao atuar como uma centralização dos dados processados coletados em campo, ele pode apresentar métricas essenciais e tendências em um
            formato visualmente intuitivo. Isso o torna uma solução ideal para órgãos ambientais que buscam adquirir elementos para a
            Detecção Precoce - Resposta Rápida e continuamente adaptar estratégias de manejo de espécies invasoras com base em dados.
            Nesta documentação exploraremos os componentes fundamentais de desenvolvimento e interpretação dos dados no Dashboard de Monitoramento e Manejo do Coral-Sol - *PACS REBIO Arvoredo.

    """),

        html.Figure([
        html.Img(src="assets/img/cora_sol.png",
                 style={"width": "50%",
                        "margin": "30px auto",
                        "display": "block",
                        "border-radius": "20px"}),
        html.Figcaption("Coral-Sol: Tubastraea coccinea.(Marcelo Crivellaro-PACS Arvoredo)", style={
            "text-align": "center",
            "color": "#aaa",
            "font-size": "1rem",
            "margin-top": "08px"
        })
    ]),



    html.Br(),
    html.Br(),

    html.H1("PROTOCOLO DE MONITORAMENTO",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #2a7ae2",
    "paddingBottom": "5px"
    }),

    html.Br(),
    html.H2("AQUISIÇÃO DAS INFORMAÇÕES EM CAMPO",
             style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #6a737a",
    "paddingBottom": "5px"
    }),

    html.Br(),
    html.H3("""
        Os dados de monitoramento são obtidos em localidades, onde é definido um segmento, e
        na extensão de um segmento são coletadas informações relacionadas a transectos visuais minuto a minuto de busca ativa.

    """),
    html.Br(),

    html.Figure([
        html.Img(src="assets/img/segmento.png",
                 style={"width": "50%",
                        "margin": "30px auto",
                        "display": "block",
                        "border-radius": "20px"}),
        html.Figcaption("Esquema de obtenção dos dados.(PACS Arvoredo)", style={
            "text-align": "center",
            "color": "#aaa",
            "font-size": "1rem",
            "margin-top": "08px"
        })
    ]),

    html.Br(),
    html.Br(),
    html.H2("BUSCA ATIVA",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #6a737a",
    "paddingBottom": "5px"
    }),

    html.Br(),
    html.H2("""
        Snorkeling
    """),
    html.Br(),
    html.H3("""
            Na faixa de profundidade de zero a 2 metros do segmento de amostragem, o monitoramento e realizado por uma dupla de mergulhadores
            em snorkeling. O mergulhador fará uma busca ativa dentro dessa faixa de profundidade, procurando possíveis ocorrências de
            coral-sol ao longo de toda a extensão do segmento de amostragem.
    """),
    html.Br(),
    html.H2("""
        Mergulho Autônomo (SCUBA)
    """),
    html.Br(),
    html.H3("""
            As amostragens com mergulho autônomo são conduzidas por duas duplas. A área operacional para cada dupla e
            determinada por faixas de profundidade (por exemplo, de 2 a 8m e de 9 a 15m) ao longo do segmento de amostragem, visando cobrir
            a maior extensão vertical possível. A divisão das profundidades de varredura entre os pares pode variar dependendo das características
            batimétricas de cada segmento de amostragem.

    """),
    html.Br(),
    html.Br(),

    html.Figure([
        html.Img(src="assets/img/monitora_dash.png",
                 style={"width": "50%",
                        "margin": "30px auto",
                        "display": "block",
                        "border-radius": "20px"}),
        html.Figcaption("Esquema operacional por batimetria no monitoramento.(PACS Arvoredo)", style={
            "text-align": "center",
            "color": "#aaa",
            "font-size": "1rem",
            "margin-top": "08px"
        })
    ]),

    html.Br(),
    html.Br(),

    html.H1("DAFOR",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #6a737a",
    "paddingBottom": "5px"
    }),
    html.Br(),
    html.Br(),

    html.H3("""
           Para classificar os níveis de invasão nos segmentos amostrados, utilizamos uma escala semi-quantitativa de abundância conhecida como escala DAFOR (Sutherland, 2006),
            especificamente adaptada para avaliar a abundância de coral-sol (Creed & Fleury, 2009). A cada transecto de 1 minuto é atribuída uma categoria  de abundância relativa,
            que são descritas da seguinte forma:
           """),
    html.Br(),
    html.Ul([
        html.Li([
            html.H3("Dominante:"),
            "Esta categoria representa populações altamente evidentes que formam predominantemente manchas monoespecíficas de pelo menos 1m². Essas manchas contêm numerosas colônias isoladas e/ou manchas menores espalhadas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.H3("Abundante: "),
            "Os agrupamentos nesta categoria formam manchas essencialmente monoespecíficas variando de 50 a 100 cm de diâmetro. Semelhante à categoria dominante, colônias isoladas e/ou pequenas manchas espalhadas podem ser observadas ao longo do substrato."
        ]),
        html.Br(),
        html.Li([
            html.H3("Frequente: "),
            "Esta classe inclui colônias isoladas e/ou pequenas manchas variando de 10 a 50 cm de diâmetro, espalhadas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.H3("Ocasional: "),
            "Esta categoria abrange casos em que entre 1 e 5 colônias estão dispersas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.H3("Raro: "),
            "Esta categoria abrange casos em que entre 1 e 5 colônias estão dispersas pelo substrato."
        ]),
        html.Br(),
        html.Li([
            html.H3("Ausente: "),
            "Sem registro de coral-sol no minuto amostrado."

        ]),
    ]),
    html.Br(),
    html.Br(),

    html.H1("ÍNDICE DE ABUNDÂNCIA RELATIVA",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #6a737a",
    "paddingBottom": "5px"
    }),
    html.Br(),

    html.H3("""
            As observações realizadas na escala DAFOR são então convertidas para um índice de abundância relativa (IAR) usando a seguinte classificação:
           10 - dominante, 8 - abundante, 6 - frequente, 4 - ocasional, 2 - raro; zero - ausente. A ilustração abaixo mostra as categorias da escala DAFOR
              e seus respectivos valores de IAR.

           """),
    html.Figure([
        html.Img(src="assets/img/dafor_pt.png",
                 style={"width": "50%",
                        "margin": "30px auto",
                        "display": "block",
                        "border-radius": "20px"}),
        html.Figcaption("Escala DAFOR utilizada nos monitoramentos (Sergio Coelho, com. pess.; CREED, et al. 2025.)", style={
            "text-align": "center",
            "color": "#aaa",
            "font-size": "1rem",
            "margin-top": "08px"
        })
    ]),
    html.Br(),
    html.Br(),
    html.H1("PROTOCOLO DE MANEJO",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #2a7ae2",
    "paddingBottom": "5px"
    }),

    html.Br(),
    html.Br(),
     html.H3("""
          O manejo do coral-sol na REBIO Arvoredo tem como objetivo reduzir a população e conter sua dispersão,
          buscando a erradicação pontual quando possível. As ações combinam estratégias de remoção em campo e
          registro padronizado das informações.
           """),
    html.Br(),
    html.Br(),
    html.H1("ESTRATÉGIAS",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #6a737a",
    "paddingBottom": "5px"
    }),
    html.Br(),
    html.Br(),
    html.Ul([
        html.Li([
            html.H3("Manejo simples: Aplicado em áreas onde a erradicação não é viável, priorizando a retirada de colônias com maior potencial reprodutivo (colônias maiores que 15 pólipos.")
        ]),
        html.Br(),

]),
html.Ul([
        html.Li([
            html.H3("Manejo combinado: utilizado em locais com possibilidade de erradicação, envolvendo a remoção de todas as colônias (independentemente do tamanho), seguida da limpeza de resíduos com escova elétrica rotativa."),
        ]),
        html.Br(),

]),
    html.Br(),
    html.Br(),
    html.H1("FERRAMENTAS DE MANEJO",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #6a737a",
    "paddingBottom": "5px"
    }),
    html.Br(),
    html.Br(),
     html.H3("""
          São empregados marteletes pneumáticos ou elétricos para remoção em áreas densamente colonizadas, e marreta, talhadeira ou formão em situações
          que exigem maior precisão ou quando há restrições ao uso de ferramentas motorizadas. A escova rotativa é usada para eliminar resíduos após a remoção.
          O material retirado deve ser recolhido com puçás ou sacos de coleta para evitar a dispersão de fragmentos.
           """),
    html.Br(),
    html.Br(),

    html.Figure([
        html.Img(src="assets/img/manejo.png",
                 style={"width": "50%",
                        "margin": "30px auto",
                        "display": "block",
                        "border-radius": "20px"}),
        html.Figcaption("Manejo realizado com talhadeira e marreta (PACS Arvoredo)", style={
            "text-align": "center",
            "color": "#aaa",
            "font-size": "1rem",
            "margin-top": "08px"
        })
    ]),

    html.Br(),
    html.Br(),
    html.H1("INDICADORES DO MONITORAMENTO E MANEJO",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #2a7ae2",
    "paddingBottom": "5px"
    }),
    html.Br(),
    html.Br(),

    html.H3("""

            Alguns indicadores foram desenvolvidos para avaliação das ações de monitoramento e manejo da invasão do coral-sol na
            REBIO Arvoredo e entorno. Os indicadores são calculados e apresentados condicionados aos filtros de período e localidade selecionados no dashboard.
            Abaixo exploramos cada um dos indicadores desenvolvidos:

           """),
    html.Br(),
    html.Ul([
        html.Li([
            html.H3("Detecções por Unidade de Esforço (DPUE)"),
            "Este indicador é calculado dividindo o número total de detecções de coral-sol pelo esforço total de amostragem, medido em minutos e unidades de tamanho da localidade. "
            "A DPUE fornece uma medida padronizada da frequência de detecção do coral-sol ao longo do tempo, permitindo a comparação entre diferentes períodos e locais de amostragem."
        ]),
        html.Br(),

        html.Li([
            html.H3("Índice de Abundância Relativa Ponderado (RAI-W)"),
            "Para incorporar a abundância relativa com ênfase nos impactos ecológicos não-lineares da dominância do coral-sol, cada pontuação DAFOR minuto a minuto (s_i ∈ {10, 8, 6, 4, 2, 0}) foi convertida em um peso manual w(s_i) que enfatiza as categorias mais altas. "
            "Os pesos manuais foram determinados por consenso de especialistas e revisão da literatura, garantindo que reflitam o impacto ecológico de densidades variadas de coral-sol. "
            "Os pesos manuais utilizados foram: w(10) = 1,00, w(8) = 0,80, w(6) = 0,60, w(4) = 0,10, w(2) = 0,04, w(0) = 0. "
            "No dashboard e nos relatórios, o indicador exibido é normalizado para a escala de 0 a 10 pela fórmula: "
            "RAI-W = 10 × [Σw(s_i) / Nmin], onde Nmin é o total de minutos monitorados. "
            "Essa normalização mantém o indicador no mesmo intervalo da escala DAFOR e facilita a comparação entre localidades e períodos."
        ]),

        html.Br(),
        html.Li([
            html.H3("DAFOR Espacial - Em desenvolvimento"),
            "Este indicador espacializa os valores DAFOR ao longo das bordas das localidades monitoradas, criando um mapa de calor de abundância do coral-sol. "
            "A metodologia divide cada localidade em segmentos de 100 metros e calcula a média ponderada dos valores DAFOR dos transectos de monitoramento próximos (dentro de um raio de 50 metros). "
            "A ponderação é feita pelo esforço de amostragem (número de minutos) de cada transecto, garantindo que segmentos com maior esforço de monitoramento contribuam proporcionalmente mais para a média. "
            "A fórmula utilizada é: DAFOR_espacial = Σ(score × esforço) / Σ(esforço). "
            "Segmentos sem dados de monitoramento próximos recebem valor 0 (Ausente). A visualização usa a escala de cores invertida vermelho-amarelo-verde (RdYlGn_r), onde vermelho indica alta abundância (Dominante), "
            "amarelo indica abundância moderada (Frequente) e verde indica baixa abundância ou ausência. Um sistema de cache melhora o desempenho ao armazenar resultados de consultas recentes."
        ]),






        html.Br(),
        html.Li([
            html.H3("Ocorrências"),
            "Este indicador apresenta no mapa as ocorrências de coral-sol por localidade, permitindo a visualização espacial da distribuição "
            "da espécie invasora e informações locais como a localidade, data, profundidade, acesso (acessível, parcialmente acessível, inacessível)"
            "e o tipo da geomorfologia em que a ocorrência foi registrada (toca ou Caverna, lage, matacão ou paredão ou rochas médias e pequenas)"
        ]),
         html.Figure([
    html.Img(src="assets/img/occ_pic.png",
             style={"width": "40%",
                    "margin": "30px auto",
                    "display": "block",
                    "border-radius": "20px"}),
    html.Figcaption("Foto das ocorrências de coral-sol inseridas no Banco de Dados", style={
        "text-align": "center",
        "color": "#aaa",
        "font-size": "1rem",
        "margin-top": "08px"
    })
]),
        html.Br(),
        html.Li([
            html.H3("Massa manejada (Kg)"),
            "Este indicador representa a quantidade total de coral-sol manejada por localidade ao longo do tempo. A massa manejada (Kg) é uma medida importante para avaliar a eficácia das ações de controle e manejo da espécie invasora."
        ]),
        html.Br(),
        html.Li([
            html.H3("Último Manejo (dias)"),
            " Este indicador mostra o número de dias desde a última ação de manejo realizada em cada localidade. Ele é útil para monitorar a frequência das intervenções e garantir que as áreas sejam manejadas regularmente para controlar a população de coral-sol."
        ]),
        html.Br(),
        html.Li([
            html.H3("Último monitoramento (dias)"),
            "Este indicador mostra o número de dias desde o último monitoramento realizado em cada localidade. Ele é útil para garantir que as áreas sejam monitoradas regularmente."
        ]),

        html.Br(),
        html.Li([
            html.H3("Trajetos de Número de monitoramentos por localidade"),
            "Este indicador mostra o número de monitoramentos realizados em cada localidade. Ele é útil para avaliar o esforço de monitoramento e identificar áreas que podem necessitar de maior atenção."
        ]),






    ]),
    html.Br(),

    html.H1("REFERÊNCIAS",
            style={
    "marginTop": "20px",
    "marginBottom": "10px",
    "borderBottom": "2px solid #2a7ae2",
    "paddingBottom": "5px"
    }),
    html.Br(),
    html.Br(),

    html.Ul([
        html.Li("COELHO-SOUZA, S. A. et al. (2025). A “short blanked” reality: The challenge to control sun coral invasion in a large no-take marine protected area over a decade of adaptive management. Marine Pollution Bulletin, 216, 117947. https://doi.org/10.1016/j.marpolbul.2025.117947"),
        html.Li("CREED, J. C. et al. 2025. A Bioinvasão do Coral-Sol. Zenodo. https://doi.org/10.5281/zenodo.16882236"),
        html.Li("CREED, J.C.; FLEURY, B.G. 2009. Monitoramento extensivo de coral-sol (Tubastraea coccinea e T. tagusensis): protocolo de semi-quantificação. Projeto Coral-Sol, Instituto Biodiversidade Marinha, Rio de Janeiro. p 1."),
        html.Li("CREED, J.C. et al. 2017. The Sun-Coral Project: the first social-environmental initiative to manage the biological invasion of Tubastraea spp. in Brazil. Management of Biological Invasions 8(2): 181."),
        html.Li("CREED, J.C. et al. 2017. The invasion of the azooxanthellate coral Tubastraea (Scleractinia: Dendrophylliidae) throughout the world: history, pathways and vectors. Biological Invasions 19: 283-305."),
        html.Li("CRIVELLARO. et al. 2024.(2020). Fighting on the edge: Reproductive effort and population structure of the invasive coral Tubastraea coccinea in its southern Atlantic limit of distribution following control activities. Biological Invasions. https://doi.org/10.1007/s10530-020-02403-5"),
        html.Li("CRISP, DJ; SOUTHWARD, AJ. 1958. The distribution of intertidal organisms along the coasts of the English Channel. Journal of the Marine Biological Association UK 37: 157-208."),
        html.Li("GRAINGER, S. et al. 2016. Environmental data visualisation for non-scientific contexts: Literature review and design framework. Environmental Modelling & Software, 85, 299-318."),
        html.Li("SILVEIRA, T.C.L. et al. 2023. Protocolo Técnico de monitoramento de coral-sol na REBIO Arvoredo e entorno. In: Protocolos Técnicos de Campo. PACS Arvoredo. Projeto PACS Arvoredo. Florianópolis, 56 p."),
        html.Li("SUTHERLAND, W.J. 2006. Ecological Census Techniques: A Handbook. 2nd edition. Cambridge University Press, Cambridge, UK."),
    ]),
    html.Br(),

        html.H1("*PACS Arvoredo",
                    style={
            "marginTop": "20px",
            "marginBottom": "10px",
            "borderBottom": "2px solid #2a7ae2",
            "paddingBottom": "5px"
            }),
    html.Br(),
    html.P("""
        O PACS Arvoredo (Plano de Ação para Prevenção e Controle do Coral-sol na REBIO Arvoredo e Entorno) é uma condicionante da Licença de Operação nº 1587/2020 emitida pelo IBAMA em 08/07/2020 referente ao Sistema de
        Desenvolvimento da Produção de Petróleo do Campo de Baúna, localizado na Bacia de Santos, sob concessão da Karoon Energy e tem como principal objetivo gerar conhecimento científico sobre a espécie
        Tubastraea coccinea (coral-sol) e o desenvolvimento de ferramentas e técnicas para a prevenção e controle desta espécie na REBIO Arvoredo e entorno.
           """),

    html.H1("Contato",
                    style={
            "marginTop": "20px",
            "marginBottom": "10px",
            "borderBottom": "2px solid #2a7ae2",
            "paddingBottom": "5px"
            }),
    html.Br(),
    html.Div([
        html.P([
            html.Strong("Para dúvidas, sugestões, relatos de erro no sistema ou mais informações sobre o monitoramento:"),
            html.Br(),
            "Thiago Cesar Lima Silveira",
            html.Br(),
            "E-mail: silveira.tcl at gmail.com",
        ], style={"marginBottom": "16px", "lineHeight": "1.7"}),
        html.P([
            html.Strong("Registros de ocorrências de coral-sol:"),
            html.Br(),
            "ICMBio NGI Florianópolis",
            html.Br(),
            "E-mail: ngi.florianopolis aticmbio.gov.br",
        ], style={"marginBottom": "0", "lineHeight": "1.7"}),
    ], style={
        "padding": "0"
    }),
    html.Br(),
    html.Hr(style={
        "border": "0",
        "borderTop": "2px solid #2a7ae2",
        "margin": "10px 0 18px 0",
        "opacity": "1"
    }),
    html.Div([
        html.Img(src="assets/img/pacs.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
        html.A(html.Img(src="assets/img/labar.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
               href="https://labarufsc.weebly.com/", target="_blank"),
        html.A(html.Img(src="assets/img/labsub.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
               href="https://lasub.ufsc.br/", target="_blank"),
        html.A(html.Img(src="assets/img/ufsc.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
               href="https://www.ufsc.br/", target="_blank"),
        html.A(html.Img(src="assets/img/feesc.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
               href="https://www.feesc.org.br/site/", target="_blank"),
        html.A(html.Img(src="assets/img/horus.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
               href="https://institutohorus.org.br/", target="_blank"),
        html.A(html.Img(src="assets/img/icmbio_br.png", style={"maxHeight": "72px", "width": "auto", "maxWidth": "180px"}),
               href="https://www.gov.br/icmbio/pt-br", target="_blank")


    ], style={
        "padding": "16px 0 24px 0",
        "display": "flex",
        "flexWrap": "wrap",
        "justifyContent": "center",
        "alignItems": "center",
        "gap": "22px"
    }),





    html.Button("Voltar", id="back-to-dashboard-btn", n_clicks=0, style={"margin-top": "30px"})
])