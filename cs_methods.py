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
            Um dashboard de dados é uma ferramenta que permite aos usuários visualizar e compreender dados complexos de forma simples.
            Ao atuar como uma centralização de dados processados, ele pode apresentar métricas essenciais e tendências em um formato visualmente intuitivo. 
            Isso o torna uma solução ideal para agências ambientais que buscam adquirir elementos para a Detecção Precoce - Resposta Rápida (DPRR) de espécies invasoras.
            Nesta documentação exploraremos os componentes fundamentais para interpretação dos dados no Dashboard de Monitoramento e Manejo do Coral-Sol - *PACS REBIO Arvoredo.
    """),

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
        na extensão de um segmento são coletadas informações relacionadas a transectos visuais de um minuto cada. 

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
            Na faixa de profundidade de zero a 2 metros do segmento de amostragem, o monitoramento será realizado por um mergulhador 
            em snorkeling. O mergulhador fará uma busca ativa dentro dessa faixa de profundidade, procurando possíveis ocorrências de 
            coral-sol ao longo de toda a extensão do segmento de amostragem. 
    """),
    html.Br(),
    html.H2("""
        Mergulho Autônomo (SCUBA)
    """),
    html.Br(),
    html.H3("""
            As amostragens com mergulho autônomo serão conduzidas por dois pares de mergulhadores. A área operacional para cada par será 
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
            especificamente adaptada para avaliar a abundância de coral-sol (Creed & Fleury, 2009). A cada transecto de 1min é atribuída uma categoria  de abundância relativa, que são descritas da seguinte forma:
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
            As observações feitas na escala DAFOR são então convertidas para um índice de abundância relativa (RAI) usando a seguinte classificação: 
           10 - dominante, 8 - abundante, 6 - frequente, 4 - ocasional, 2 - raro; zero - ausente. A ilustração abaixo ilustra as categorias da escala DAFOR
              e seus respectivos valores de RAI.
        
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
           Alguns indicadores foram desenvolvidos para avaliação das das ações de monitoramento e manejo da invasão do coral-sol na 
            REBIO Arvoredo e entorno Abaixo exploramos cada um dos indicadores desenvolvidos:

           """),
    html.Br(),
    html.Ul([
        html.Li([
            html.H3("Detecçoes por Unidade de Esforço (DPUE)"),
            "Este indicador é calculado dividindo o número total de detecções de coral-sol pelo esforço total de amostragem, medido em minutos e unidades de tamanho da localidade. O DPUE fornece uma medida padronizada da frequência de detecção do coral-sol ao longo do tempo, permitindo a comparação entre diferentes períodos e locais de amostragem."
        ]),
        html.Br(),
        html.Li([
            html.H3("Indice de Abundância Relativa (IAR-DAFOR)"),
            " Este indicador é derivado da escala DAFOR, que classifica a abundância do coral-sol em categorias qualitativas (Dominante, Abundante, Frequente, Ocasional, Raro, Ausente).  "
            " Para cada categoria é atribuída a um valor numérico específico. Nos gráficos, o IAR-DAFOR é representado pela soma dos valores de IAR (Índice de Abundância Relativa) por localidade. Também é possível observar a distribuição das categorias DAFOR por uma ou mais localidades." 
        ]),
        html.Br(),
        html.Li([
            html.H3("Ocorrências"),
            "Este indicador apresenta no mapa as ocorrências de coral-sol por localidade, permitindo a visualização espacial da distribuição "
            "da espécie invasora e informações locais como a localidade, data, profundidade, acesso (acessível, parcialmente acessível, inacessível)"
            " e o tipo da geomorfologia em que a ocorrência foi registrada (toca ou Caverna, lage, matacão ou paredão ou rochas médias e pequenas)"
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
            html.H3("Massa manejada"),
            "Este indicador representa a quantidade total de coral-sol manejada por localidade ao longo do tempo. A massa manejada é uma medida importante para avaliar a eficácia das ações de controle e manejo da espécie invasora."
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
            html.H3("Número de monitoramentos por localidade"),
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
        html.Li("CREED, J. C. et al. 2025. A Bioinvasão do Coral-Sol. Zenodo. https://doi.org/10.5281/zenodo.16882236"),
        html.Li("CREED, J.C.; FLEURY, B.G. 2009. Monitoramento extensivo de coral-sol (Tubastraea coccinea e T. tagusensis): protocolo de semi-quantificação. Projeto Coral-Sol, Instituto Biodiversidade Marinha, Rio de Janeiro. p 1."),
        html.Li("CREED, J.C. et al. 2017. The Sun-Coral Project: the first social-environmental initiative to manage the biological invasion of Tubastraea spp. in Brazil. Management of Biological Invasions 8(2): 181."),
        html.Li("CREED, J.C. et al. 2017. The invasion of the azooxanthellate coral Tubastraea (Scleractinia: Dendrophylliidae) throughout the world: history, pathways and vectors. Biological Invasions 19: 283-305."),
        html.Li("SCRISP, DJ; SOUTHWARD, AJ. 1958. The distribution of intertidal organisms along the coasts of the English Channel. Journal of the Marine Biological Association UK 37: 157-208."),
        html.Li("GRAINGER, S. et al. 2016. Environmental data visualisation for non-scientific contexts: Literature review and design framework. Environmental Modelling & Software, 85, 299-318."),
        html.Li("SILVEIRA, T.C.L. et al. 2023. Protocolo Técnico de monitoramento de coral-sol na REBIO Arvoredo e entorno. In: Protocolos Técnicos de Campo. PACS Arvoredo. Projeto PACS Arvoredo. Florianópolis, 56 p."),
        html.Li("SUTHERLAND, W.J. 2006. Ecological Census Techniques: A Handbook. 2nd edition. Cambridge University Press, Cambridge, UK."),
    ]),
    html.Br(),

    html.H3("*PACS Arvoredo"),
    html.P("""
        O PACS Arvoredo (Plano de Ação para Prevenção e Controle do Coral-sol na REBIO Arvoredo e Entorno) é uma condicionante da Licença de Operação nº 1587/2020 emitida pelo IBAMA em 08/07/2020 referente ao Sistema de 
        Desenvolvimento da Produção de Petróleo do Campo de Baúna, localizado na Bacia de Santos, sob concessão da Karoon Energy e tem como principal objetivo gerar conhecimento científico sobre a espécie 
        Tubastraea coccinea (coral-sol) e o desenvolvimento de ferramentas e técnicas para a prevenção e controle desta espécie na REBIO Arvoredo e entorno.
           """),




    html.Button("Voltar", id="back-to-dashboard-btn", n_clicks=0, style={"margin-top": "30px"})
])