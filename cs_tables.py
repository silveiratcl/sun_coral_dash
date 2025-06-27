from dash import dash_table
from dash import html

def build_occurrences_table(df):
    if df.empty:
        return html.Div("Nenhum dado disponível.")
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={
            'overflowX': 'auto',
            'backgroundColor': '#222',
            'borderRadius': '8px',
            'padding': '10px'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '8px',
            'backgroundColor': '#222',
            'color': 'white',
            'border': '1px solid #444',
            'fontFamily': 'Roboto, Arial, sans-serif',
            'fontSize': '16px'
        },
        style_header={
            'backgroundColor': '#111',
            'color': 'white',
            'fontWeight': 'bold',
            'border': '1px solid #444',
            'fontSize': '17px'
        },
        style_data={
            'backgroundColor': '#222',
            'color': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#282828'
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': '#333',
                'color': 'white'
            }
        ],
        page_size=10,
    )