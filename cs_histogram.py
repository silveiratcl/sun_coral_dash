from dash import dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px


def build_histogram_figure(dpue_df):
    """
    Builds a histogram figure for DPUE values using Plotly Express.
    """
    
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
    """
    Builds a horizontal bar chart for DPUE values by locality using Plotly Express.
    """
    
    #import plotly.express as px
    #import plotly.graph_objects as go

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

def build_dafor_histogram_figure(dafor_values):
    """
    Builds a histogram figure for DAFOR values using Plotly Express,
    mapping numeric values to DAFOR scale labels.
    """
    # Handle empty or all-NaN DAFOR values
    if dafor_values.empty or dafor_values.dropna().empty:
        return go.Figure()  # Return an empty figure

    # Define the mapping
    dafor_map = {
        10: "D",
        8: "A",
        6: "F",
        4: "O",
        2: "R",
        0: "Ausente"
    }

    # Map numeric values to labels, keep only defined values
    dafor_labels = dafor_values.map(dafor_map).dropna()

    # Define the order for the categories
    category_order = [ "D", "A", "F", "O", "R", "Ausente"]

    fig = px.histogram(
        x=dafor_labels,
        category_orders={"x": category_order},
        template="plotly_dark",
    )

    fig.update_layout(
        bargap=0.1,
        margin={"r":10,"t":20,"l":10,"b":40},
        height=180,
        yaxis_title="Contagem",
        xaxis_title="IAR-DAFOR",
    )
    return fig


def build_dafor_sum_bar_figure(df_dafor_sum):
    """
    Builds a horizontal bar chart for the sum of DAFOR values by locality using Plotly Express.
    Expects a DataFrame with columns: ['locality_id', 'name', 'date', 'DAFOR'].
    """
    import plotly.express as px
    import plotly.graph_objects as go

    if df_dafor_sum.empty or df_dafor_sum["DAFOR"].dropna().empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Soma DAFOR",
            yaxis_title=None,
            yaxis_showticklabels=False,
            margin={"r":10,"t":20,"l":10,"b":40},
            height=300
        )
        return fig

    # Group by locality to get the total sum per locality (across all dates)
    df_grouped = df_dafor_sum.groupby(['locality_id', 'name'], as_index=False)['DAFOR'].sum()
    df_grouped = df_grouped[df_grouped["DAFOR"] > 0]
    df_grouped = df_grouped.sort_values("DAFOR", ascending=False)

    # Ensure 'name' is string and categorical for ordering
    df_grouped['name'] = df_grouped['name'].astype(str)
    df_grouped['name'] = pd.Categorical(df_grouped['name'], categories=df_grouped['name'], ordered=True)

    fig = px.bar(
        df_grouped,
        x="DAFOR",
        y="name",
        orientation="h",
        template="plotly_dark",
        labels={"DAFOR": "Soma DAFOR por Localidade", "name": "Localidade"},
        text="name",
    )
    fig.update_traces( insidetextanchor='start')
    #fig.update_traces(textposition='inside', insidetextanchor='middle')
    fig.update_layout(
        yaxis=dict(autorange="reversed", showticklabels=False),
        yaxis_title=None,
        margin={"r":10,"t":20,"l":10,"b":40},
        height=500
    )
    return fig

def build_accumulated_mass_year_figure(df_management):
    """Builds a line chart by locality for accumulated mass managed by year using Plotly Express."""
    import plotly.express as px

    if df_management.empty:
        return go.Figure()

    # Ensure 'name' is present and not NaN
    df_management = df_management.dropna(subset=['name'])
    df_management['year'] = pd.to_datetime(df_management['date']).dt.year

    df_grouped = df_management.groupby(['locality_id', 'name', 'year'], as_index=False)['managed_mass_kg'].sum()
    df_grouped = df_grouped[df_grouped['managed_mass_kg'] > 0]

    print(df_grouped)  # Debug: check if you have multiple localities and years

    fig = px.line(
        df_grouped,
        x='year',
        y='managed_mass_kg',
        color='name',
        title="Massa Manejada Acumulada por Ano",
        labels={"managed_mass_kg": "Massa Manejada (kg)", "year": "Ano"},
        template="plotly_dark"
    )

    fig.update_layout(
        yaxis_title="Massa Manejada (kg)",
        xaxis_title="Ano",
        margin={"r":10,"t":30,"l":10,"b":40},
        height=500
    )
    return fig