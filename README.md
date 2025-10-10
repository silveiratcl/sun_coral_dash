

# Sun Coral Dashboard

Este é um painel interativo desenvolvido em Python para o monitoramento e manejo do coral-sol (*Tubastraea spp.*) na REBIO Arvoredo e entorno. O dashboard integra dados de campo, ações de manejo e indicadores ecológicos, facilitando a visualização e análise para pesquisadores e gestores ambientais.

## 🔧 Funcionalidades

- Visualização de mapas interativos:
  - Detecção por Unidade de Esforço (DPUE)
  - Índice de Abundância Relativa (IAR-DAFOR)
  - Ocorrências georreferenciadas com fotos
  - Dias desde o último manejo ou monitoramento
  - Massa total manejada por localidade
- Gráficos de barras e histogramas DAFOR
- Documentação dos protocolos de monitoramento e manejo
- Referências científicas e links úteis

## 💻 Estrutura do Projeto

- `cs_index.py`: Arquivo principal do Dash, gerencia layout e navegação
- `cs_map.py`: Funções para mapas interativos
- `cs_histogram.py`: Funções para gráficos DAFOR
- `cs_methods.py`: Documentação e protocolos
- `services/data_service.py`: Consulta e processamento dos dados
- `assets/`: Imagens e arquivos estáticos

## 🚀 Como Executar

1. Instale as dependências:
   ```sh
   pip install dash plotly pandas numpy sqlalchemy geopy dash-bootstrap-components matplotlib
   ```
2. Configure a conexão com o banco em `config/database.py`
3. Execute o aplicativo:
   ```sh
   python cs_index.py
   ```

## 👨‍💻 Tecnologias Utilizadas

- Python
- Dash
- Plotly
- Pandas
- NumPy
- SQLAlchemy
- Geopy
- Dash Bootstrap Components
- Matplotlib

## 📜 Referências

- Creed et al. (2025). *A bioinvasão do Coral-Sol. in press.*
- Sutherland, W.J. (2006). *Ecological Census Techniques: A Handbook.*
- Veja `cs_methods.py` para a bibliografia completa.

## 🤝 Suporte/Contato

Para dúvidas ou contribuições, entre em contato com os mantenedores do projeto ou abra uma issue no repositório.

---

<p align="center">Copyright © 2024 Projeto Sun Coral Dashboard</p>
