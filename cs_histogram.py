from dash import dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px


def build_histogram_figure(dpue_df):
    import plotly.express as px

    # Handle empty or all-NaN DPUE
    if dpue_df.empty or dpue_df["DPUE"].dropna().empty:
        return go.Figure()  # Return an empty figure
    
    min_dpue = dpue_df["DPUE"].min()
    max_dpue = dpue_df["DPUE"].max()
    if pd.isna(min_dpue) or pd.isna(max_dpue):
        return go.Figure()  # Return an empty figure

    nbins = int((max_dpue - min_dpue) / 0.5) + 1

    fig = px.histogram(
        dpue_df,
        x="DPUE",
        nbins=nbins,
        template="plotly_dark",   
    )

    fig.update_layout(
         bargap=0.1,
         margin={"r":10,"t":20,"l":10,"b":40},
         height=180, 
         yaxis_title="Contagem",
    )
    return fig

def build_locality_bar_figure(dpue_df):
    import plotly.express as px
    import plotly.graph_objects as go

    if dpue_df.empty or dpue_df["DPUE"].dropna().empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="DPUE",
            yaxis_title="Localidade",
            margin={"r":10,"t":20,"l":10,"b":40},
            height=300
        )
        return fig

    # Filter for DPUE > 0 and sort descending
    df_sorted = dpue_df.dropna(subset=["DPUE"])
    df_sorted = df_sorted[df_sorted["DPUE"] > 0]
    df_sorted = df_sorted.sort_values("DPUE", ascending=False)
    y_col = "name" if "name" in df_sorted.columns else "locality_id"

    df_sorted[y_col] = df_sorted[y_col].astype(str)
    df_sorted[y_col] = pd.Categorical(df_sorted[y_col], categories=df_sorted[y_col], ordered=True)

    fig = px.bar(
        df_sorted,
        x="DPUE",
        y=y_col,
        orientation="h",
        template="plotly_dark",
        labels={"DPUE": "DPUE"},
        text=y_col,
    )
    #fig.update_traces(textposition='inside', insidetextanchor='start')
    fig.update_traces( insidetextanchor='start')
    fig.update_layout(
        yaxis=dict(autorange="reversed", showticklabels=False),
        yaxis_title=None,
        margin={"r":10,"t":20,"l":10,"b":40},
        height=500
    )
    return fig
