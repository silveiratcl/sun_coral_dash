from dash import dash_table
import dash_html_components as html

def build_occurrences_table(df):
    if df.empty:
        return html.Div("Nenhum dado disponível.")
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': '#222', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'backgroundColor': '#333', 'color': 'white'},
        page_size=10,
    )