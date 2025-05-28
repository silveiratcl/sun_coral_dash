from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px


def build_histogram_figure(dpue_df):
    # Set bin size to 0.5
    fig = px.histogram(
        dpue_df,
        x="DPUE",
        nbins=int((dpue_df["DPUE"].max() - dpue_df["DPUE"].min()) / 0.5) + 1,
        #title="Distribuição do DPUE",
        labels={"DPUE": "DPUE"},
        template="plotly_dark"
    )
    fig.update_traces(xbins=dict(
        start=dpue_df["DPUE"].min(),
        end=dpue_df["DPUE"].max(),
        size=0.5
    ))
    fig.update_layout(
        bargap=0.1,
        margin={"r":10,"t":20,"l":10,"b":40},
        height=180, 
        yaxis_title="Contagem",

        

    )
    return fig