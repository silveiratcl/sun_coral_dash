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
        title="Densidade de DPUE",
        nbins=nbins,
        template="plotly_dark",   
    )

    fig.update_layout(
         bargap=0.1,
         margin={"r":10,"t":35,"l":10,"b":40},
         title={
        "text": "Densidade de DPUE",
        "x": 0,  # Left justify
        "xanchor": "left"
    },
         
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
        title="Total DPUE por Localidade",
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
        title={
        "text": "Total DPUE por Localidade",
        "x": 0,  # Left justify
        "xanchor": "left"
    },
        margin={"r":10,"t":35,"l":10,"b":40},
        height=500
    )
    return fig

def build_dafor_histogram_figure(dafor_values):
    """
    Builds a histogram figure for DAFOR values using Plotly Express,
    always showing all 6 DAFOR categories, even if some are absent.
    """
    import pandas as pd
    import plotly.express as px

    # Define the mapping and order
    dafor_map = {
        10: "D",
        8: "A",
        6: "F",
        4: "O",
        2: "R",
        0: "Ausente"
    }
    category_order = ["D", "A", "F", "O", "R", "Ausente"]

    # Map numeric values to labels
    dafor_labels = dafor_values.map(dafor_map)
    dafor_labels = pd.Categorical(dafor_labels, categories=category_order, ordered=True)

    # Count occurrences, including zeros
    counts = pd.value_counts(dafor_labels, sort=False).reindex(category_order, fill_value=0)
    df_plot = pd.DataFrame({'DAFOR': category_order, 'Count': counts.values})

    fig = px.bar(
        df_plot,
        x="DAFOR",
        y="Count",
        category_orders={"DAFOR": category_order},
        template="plotly_dark",
    )

    fig.update_layout(
        bargap=0.1,
        title={
            "text": "Densidade das categorias de DAFOR",
            "x": 0,
            "xanchor": "left"
        },
        margin={"r": 10, "t": 35, "l": 10, "b": 40},
        height=180,
        yaxis_title="Contagem",
        xaxis_title="IAR-DAFOR",
    )
    return fig


def build_dafor_sum_bar_figure(df_dafor_sum):
    """
    Builds a stacked horizontal bar chart for the sum of DAFOR values by locality and DAFOR category.
    Only includes localities with total DAFOR > 0 and excludes the 'Ausente' category.
    Expects columns: ['locality_id', 'name', 'date', 'DAFOR'] where DAFOR is numeric.
    """
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    dafor_num_to_label = {
        10: "D", 8: "A", 6: "F", 4: "O", 2: "R"
        # 0: "Ausente"  # Exclude Ausente
    }
    category_order = [10, 8, 6, 4, 2]
    category_labels = [dafor_num_to_label[v] for v in category_order]

    def map_to_category(val):
        return min(category_order, key=lambda x: abs(x - val))

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

    df = df_dafor_sum.copy()
    df = df[df["DAFOR"] > 0]  # Exclude Ausente and zero values
    df["DAFOR_CAT"] = df["DAFOR"].apply(map_to_category)
    df["DAFOR_CLASS"] = df["DAFOR_CAT"].map(dafor_num_to_label)

    df_grouped = (
        df.groupby(['name', 'DAFOR_CLASS'], as_index=False)['DAFOR'].sum()
    )

    pivot = df_grouped.pivot(index='name', columns='DAFOR_CLASS', values='DAFOR').fillna(0)

    for label in category_labels:
        if label not in pivot.columns:
            pivot[label] = 0

    pivot = pivot[category_labels]
    pivot["total"] = pivot.sum(axis=1)
    pivot = pivot[pivot["total"] > 0]  # Only localities with total > 0
    pivot = pivot.sort_values("total", ascending=False)

    df_long = pivot.reset_index().melt(id_vars=["name", "total"], value_vars=category_labels,
                                       var_name="DAFOR_CLASS", value_name="SUM")

    df_long['name'] = pd.Categorical(df_long['name'], categories=pivot.index, ordered=True)
    df_long['DAFOR_CLASS'] = pd.Categorical(df_long['DAFOR_CLASS'], categories=category_labels, ordered=True)

    fig = px.bar(
        df_long,
        x="SUM",
        y="name",
        color="DAFOR_CLASS",
        orientation="h",
        template="plotly_dark",
        labels={"SUM": "Soma DAFOR por Localidade", "name": "Localidade", "DAFOR_CLASS": "Categoria DAFOR"},
        category_orders={"DAFOR_CLASS": category_labels},
        text="SUM",
    )
    fig.update_layout(
        barmode="stack",
        yaxis=dict(autorange="reversed", showticklabels=True),
        yaxis_title=None,
        title={
            "text": "Soma das pontuações DAFOR por localidade (sem categoria Ausente)",
            "x": 0,
            "xanchor": "left"
        },
        margin={"r":10,"t":35,"l":10,"b":40},
        height=500,
        legend_title_text="Categoria DAFOR"
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

    df_grouped = (
        df_management.groupby(['locality_id', 'name', 'year'], as_index=False)['managed_mass_kg'].sum()
    )
    df_grouped = df_grouped.sort_values(['locality_id', 'year'])
    df_grouped['accum_mass_kg'] = df_grouped.groupby('locality_id')['managed_mass_kg'].cumsum()
    df_grouped = df_grouped[df_grouped['accum_mass_kg'] > 0]

    print(df_grouped)  # Debug: check if you have multiple localities and years

    fig = px.line(
        df_grouped,
        x='year',
        y='accum_mass_kg',
        color='name',
        title="Massa Manejada Acumulada Anual",
        labels={"managed_mass_kg": "Massa Manejada (kg)", "year": "Ano"},
        template="plotly_dark"
    )

    fig.update_layout(
        yaxis_title="Massa Manejada (kg)",
        xaxis_title="Ano",
        title={
            "text": "Massa Manejada Acumulada Anual por Localidade",
            "x": 0,  # Left justify
            "xanchor": "left"
        },
        margin={"r":10,"t":30,"l":10,"b":40},
        height=500,
        legend_title_text=None
    )
    return fig

import plotly.express as px

def build_days_since_management_bar_figure(df_days_since):
    """
    Builds a horizontal bar chart for days since last management per locality,
    ordered from biggest to smallest.
    """
    import plotly.express as px

    # Sort by days_since descending
    df_sorted = df_days_since.sort_values("days_since", ascending=True)

    # Set categorical order for y-axis
    df_sorted['name'] = pd.Categorical(df_sorted['name'], categories=df_sorted['name'], ordered=True)

    fig = px.bar(
        df_sorted,
        x='days_since',      # Value on x-axis
        y='name',            # Locality on y-axis
        orientation='h',     # Horizontal bars
        labels={'name': 'Localidade', 'days_since': 'Dias desde última gestão'},
        title='Dias desde último manejo por localidade',
        template='plotly_dark'
    )
    fig.update_layout(
        bargap=0.2,
        margin={"r":10,"t":35,"l":10,"b":40},
        height=400,
        xaxis_title="Último Manejo (dias)",
        yaxis_title="Localidade"
    )
    return fig

def build_days_since_monitoring_bar_figure(df_days_since):
    import plotly.express as px
    df_sorted = df_days_since.sort_values("days_since", ascending=True)
    df_sorted['name'] = pd.Categorical(df_sorted['name'], categories=df_sorted['name'], ordered=True)
    fig = px.bar(
        df_sorted,
        x='days_since',
        y='name',
        orientation='h',
        labels={'name': 'Localidade', 'days_since': 'Dias desde último monitoramento'},
        title='Dias desde último monitoramento por localidade',
        template='plotly_dark'
    )
    fig.update_layout(
        bargap=0.2,
        margin={"r":10,"t":35,"l":10,"b":40},
        height=800,
        xaxis_title="Dias desde último monitoramento",
        yaxis_title="Localidade"
    )
    return fig

def build_removal_ratio_year_figure(df_management):
    """
    Builds a line chart showing the removal ratio (mass removed per day)
    grouped by year and locality.
    """
    import plotly.express as px
    import plotly.graph_objects as go

    if df_management.empty:
        return go.Figure()

    # Ensure 'name' is present and not NaN
    df_management = df_management.dropna(subset=['name'])
    df_management['year'] = pd.to_datetime(df_management['date']).dt.year

    # Group by locality and year, calculate total mass and number of days
    df_grouped = (
        df_management.groupby(['locality_id', 'name', 'year'], as_index=False)
        .agg(
            total_mass=('managed_mass_kg', 'sum'),
            n_days=('date', lambda x: x.nunique())
        )
    )
    # Calculate removal ratio (mass removed per day)
    df_grouped['removal_ratio_kg_day'] = df_grouped['total_mass'] / df_grouped['n_days']
    df_grouped = df_grouped[df_grouped['removal_ratio_kg_day'] > 0]

    fig = px.line(
        df_grouped,
        x='year',
        y='removal_ratio_kg_day',
        color='name',
        title="Razão de Remoção de Massa por Dia (kg/dia) por Ano",
        labels={"removal_ratio_kg_day": "Massa Removida/Dia (kg/dia)", "year": "Ano"},
        template="plotly_dark"
    )

    fig.update_layout(
        yaxis_title="Massa Removida/Dia (kg/dia)",
        xaxis_title="Ano",
        title={
            "text": "Razão de Remoção de Massa por Dia por Localidade e Ano",
            "x": 0,
            "xanchor": "left"
        },
        margin={"r":10,"t":30,"l":10,"b":40},
        height=500,
        legend_title_text=None
    )
    return fig

def build_monitoring_events_bar_figure(events_df):
    """
    Builds a horizontal bar chart showing the number of monitoring events per locality.
    Similar to DPUE bar chart but showing event counts.
    
    Args:
        events_df: DataFrame with locality_id, name, and event_count columns
    """
    if events_df.empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Número de Eventos",
            yaxis_title="Localidade",
            margin={"r":10,"t":20,"l":10,"b":40},
            height=300
        )
        return fig
    
    # Sort by event count descending
    df_sorted = events_df[events_df['event_count'] > 0].copy()
    df_sorted = df_sorted.sort_values('event_count', ascending=False)
    
    y_col = "name" if "name" in df_sorted.columns else "locality_id"
    df_sorted[y_col] = df_sorted[y_col].astype(str)
    df_sorted[y_col] = pd.Categorical(df_sorted[y_col], categories=df_sorted[y_col], ordered=True)
    
    fig = px.bar(
        df_sorted,
        x="event_count",
        y=y_col,
        orientation="h",
        template="plotly_dark",
        labels={"event_count": "Número de Eventos", y_col: "Localidade"},
        text=y_col,
    )
    
    fig.update_traces(insidetextanchor='start')
    fig.update_layout(
        yaxis=dict(autorange="reversed", showticklabels=False),
        yaxis_title=None,
        xaxis_title="Número de Eventos de Monitoramento",
        title={
            "text": "Eventos de Monitoramento por Localidade",
            "x": 0,
            "xanchor": "left"
        },
        margin={"r":10,"t":35,"l":10,"b":40},
        height=500
    )
    
    return fig


def build_monitoring_events_histogram_figure(events_df):
    """
    Builds a histogram showing the distribution of monitoring event counts.
    
    Args:
        events_df: DataFrame with event_count column
    """
    if events_df.empty or events_df["event_count"].dropna().empty:
        return go.Figure()
    
    fig = px.histogram(
        events_df,
        x="event_count",
        title="Distribuição de Eventos de Monitoramento",
        template="plotly_dark",
        labels={"event_count": "Número de Eventos"}
    )
    
    fig.update_layout(
        bargap=0.1,
        margin={"r":10,"t":35,"l":10,"b":40},
        title={
            "text": "Distribuição de Eventos de Monitoramento",
            "x": 0,
            "xanchor": "left"
        },
        height=180,
        yaxis_title="Contagem",
        xaxis_title="Número de Eventos"
    )
    
    return fig
