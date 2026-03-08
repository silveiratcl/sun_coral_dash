"""
Relatório em Tempo Real - Real-time report layout with detailed analyses
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from services.data_service import CoralDataService
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def create_summary_statistics():
    """Generate summary statistics cards - values updated by callback."""
    # Create cards with IDs that will be updated by callback
    cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="report-total-localities", children="0", className="card-title text-center", 
                            style={"color": "#007bff", "fontWeight": "bold"}),
                    html.P("Localidades Monitoradas", className="card-text text-center", 
                           style={"color": "#6c757d"}),
                ])
            ], color="primary", outline=True, style={"backgroundColor": "#1a1a1a"})
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="report-total-mass", children="0 kg", className="card-title text-center",
                            style={"color": "#28a745", "fontWeight": "bold"}),
                    html.P("Massa Total Manejada", className="card-text text-center",
                           style={"color": "#6c757d"}),
                ])
            ], color="success", outline=True, style={"backgroundColor": "#1a1a1a"})
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="report-total-occurrences", children="0", className="card-title text-center",
                            style={"color": "#ffc107", "fontWeight": "bold"}),
                    html.P("Ocorrências Registradas", className="card-text text-center",
                           style={"color": "#6c757d"}),
                ])
            ], color="warning", outline=True, style={"backgroundColor": "#1a1a1a"})
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="report-avg-dpue", children="0.00", className="card-title text-center",
                            style={"color": "#17a2b8", "fontWeight": "bold"}),
                    html.P("DPUE Médio Geral", className="card-text text-center",
                           style={"color": "#6c757d"}),
                ])
            ], color="info", outline=True, style={"backgroundColor": "#1a1a1a"})
        ], width=3),
    ], className="mb-4")
    
    return cards


def create_temporal_evolution_chart():
    """Create stacked chart showing temporal evolution of transects with and without sun coral."""
    service = CoralDataService()
    
    # Get DAFOR data with dates (raw data, not aggregated)
    dafor_data = service.get_dafor_data(None, None)
    
    if dafor_data.empty:
        return go.Figure().update_layout(
            title="Sem dados disponíveis",
            height=400
        )
    
    # Parse dates and aggregate by year-month
    dafor_data['date'] = pd.to_datetime(dafor_data['date'], dayfirst=True, errors='coerce')
    dafor_data = dafor_data.dropna(subset=['date'])
    dafor_data['year_month'] = dafor_data['date'].dt.to_period('M').astype(str)
    
    # Process dafor_value: split comma-separated values and explode to count individual 1-minute transects
    dafor_data['dafor_value_list'] = dafor_data['dafor_value'].apply(
        lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',') if str(i).strip()]
    )
    dafor_data = dafor_data.explode('dafor_value_list')
    dafor_data['dafor_value_list'] = pd.to_numeric(dafor_data['dafor_value_list'], errors='coerce')
    dafor_data = dafor_data.dropna(subset=['dafor_value_list'])
    
    # Check for detections (dafor_value > 0)
    dafor_data['has_detection'] = dafor_data['dafor_value_list'] > 0
    
    # Group by month and count individual transects with and without detections
    temporal_agg = dafor_data.groupby('year_month').apply(
        lambda df: pd.Series({
            'Com Coral': df['has_detection'].sum(),  # Individual 1-minute transects with dafor_value > 0
            'Sem Coral': (~df['has_detection']).sum()  # Individual 1-minute transects without detections
        })
    ).reset_index()
    temporal_agg.columns = ['Período', 'Com Coral', 'Sem Coral']
    
    # Create stacked bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=temporal_agg['Período'],
        y=temporal_agg['Com Coral'],
        name='Com Coral',
        marker_color='#FF6B6B',
        hovertemplate='<b>%{x}</b><br>Com Coral: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=temporal_agg['Período'],
        y=temporal_agg['Sem Coral'],
        name='Sem Coral',
        marker_color='#4ECDC4',
        hovertemplate='<b>%{x}</b><br>Sem Coral: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Evolução Temporal - Transectos com e sem Coral",
        xaxis=dict(title="Período (Ano-Mês)"),
        yaxis=dict(title="N° de Transectos (1 minuto cada)"),
        barmode='stack',
        hovermode='x unified',
        height=450,
        template='plotly_white',
        legend=dict(x=0.01, y=0.99)
    )
    
    return fig


def create_occurrence_by_year_chart():
    """Create bar chart showing number of occurrences marked per year."""
    service = CoralDataService()
    
    # Get occurrence data
    occurrence_data = service.get_occurrences_data(None, None)
    
    if occurrence_data.empty:
        return go.Figure().update_layout(
            title="Sem dados de ocorrências disponíveis",
            height=400
        )
    
    # Extract year from date
    occurrence_data['year'] = occurrence_data['date'].dt.year
    
    # Count occurrences by year
    yearly_counts = occurrence_data.groupby('year').size().reset_index(name='count')
    yearly_counts = yearly_counts.sort_values('year')
    
    # Create bar chart
    fig = go.Figure(go.Bar(
        x=yearly_counts['year'],
        y=yearly_counts['count'],
        marker_color='#FFB347',
        text=yearly_counts['count'],
        textposition='auto',
        hovertemplate='<b>Ano: %{x}</b><br>Ocorrências: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Marcação de Ocorrências por Ano",
        xaxis_title="Ano",
        yaxis_title="N° de Ocorrências",
        height=450,
        template='plotly_white',
        xaxis=dict(
            tickmode='linear',
            dtick=1
        )
    )
    
    return fig


def create_locality_ranking_chart():
    """Create chart ranking localities by DPUE."""
    service = CoralDataService()
    
    dpue_data = service.get_dpue_by_locality(None, None)
    
    if dpue_data.empty:
        return go.Figure()
    
    # Sort by DPUE descending
    top_localities = dpue_data.nlargest(15, 'DPUE')
    
    fig = go.Figure(go.Bar(
        x=top_localities['DPUE'],
        y=top_localities['name'],
        orientation='h',
        marker=dict(
            color=top_localities['DPUE'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="DPUE")
        ),
        text=top_localities['DPUE'].round(2),
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Top 15 Localidades por DPUE (Todas as Datas)",
        xaxis_title="DPUE (Detecções por Unidade de Esforço)",
        yaxis_title="Localidade",
        height=600,
        template='plotly_white',
        yaxis=dict(autorange="reversed")
    )
    
    return fig


def create_management_efficiency_chart():
    """Create chart showing management effort over time."""
    service = CoralDataService()
    
    management_data = service.get_management_data(None, None)
    
    if management_data.empty:
        return go.Figure().update_layout(title="Sem dados de manejo disponíveis", height=400)
    
    management_data.columns = management_data.columns.str.lower()
    management_data['date'] = pd.to_datetime(management_data['date'], dayfirst=True, errors='coerce')
    management_data = management_data.dropna(subset=['date'])
    management_data['year'] = management_data['date'].dt.year
    
    # Aggregate by year
    yearly_management = management_data.groupby('year').agg({
        'managed_mass_kg': 'sum',
        'management_id': 'count',
        'number_of_divers': 'sum'
    }).reset_index()
    yearly_management.columns = ['year', 'managed_mass_kg', 'n_events', 'total_divers']
    
    # Calculate efficiency proxy: kg per management event
    yearly_management['kg_per_event'] = yearly_management['managed_mass_kg'] / yearly_management['n_events']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=yearly_management['year'],
        y=yearly_management['managed_mass_kg'],
        name='Massa Manejada (kg)',
        marker_color='green',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_management['year'],
        y=yearly_management['n_events'],
        name='N° Eventos de Manejo',
        mode='lines+markers',
        marker=dict(size=10, color='orange'),
        line=dict(width=3),
        yaxis='y2'
    ))
    
    # Find years with mechanical methods
    mechanical_years = management_data[
        management_data['method'].str.contains('mecanizado', case=False, na=False)
    ]['year'].unique()
    
    fig.update_layout(
        title="Esforço de Manejo ao Longo dos Anos",
        xaxis=dict(title="Ano"),
        yaxis=dict(title="Massa Manejada (kg)", side='left'),
        yaxis2=dict(title="N° Eventos de Manejo", side='right', overlaying='y'),
        hovermode='x unified',
        height=450,
        template='plotly_white',
        legend=dict(x=0.01, y=0.99)
    )
    
    # Add red arrows to indicate mechanical methods
    for year in mechanical_years:
        fig.add_annotation(
            x=year,
            y=1.05,
            yref='paper',
            text='',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='red',
            ax=0,
            ay=-30
        )
    
    return fig


def create_dafor_distribution_chart():
    """Create chart showing DAFOR score distribution."""
    service = CoralDataService()
    
    dafor_data = service.get_dafor_data(None, None)
    
    if dafor_data.empty:
        return go.Figure()
    
    # Process DAFOR values
    if dafor_data['dafor_value'].apply(lambda x: isinstance(x, str) and ',' in x).any():
        dafor_data['dafor_value'] = dafor_data['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        dafor_values = pd.Series([v for sublist in dafor_data['dafor_value'] for v in sublist])
    else:
        dafor_values = pd.to_numeric(dafor_data['dafor_value'], errors='coerce')
    
    dafor_values = dafor_values.dropna()
    dafor_values = dafor_values[(dafor_values >= 0) & (dafor_values <= 10)]
    
    # Count occurrences
    value_counts = dafor_values.value_counts().sort_index()
    
    # Map to labels
    dafor_labels = {
        0: '0 - Ausente',
        2: '2 - Raro',
        4: '4 - Ocasional',
        6: '6 - Frequente',
        8: '8 - Abundante',
        10: '10 - Dominante'
    }
    
    # Define proper order for DAFOR categories (reversed - from Dominante to Ausente)
    dafor_order = [10, 8, 6, 4, 2, 0]
    ordered_labels = [dafor_labels[val] for val in dafor_order if val in value_counts.index]
    ordered_values = [value_counts[val] for val in dafor_order if val in value_counts.index]
    ordered_colors = [val for val in dafor_order if val in value_counts.index]
    
    fig = go.Figure(go.Bar(
        x=ordered_labels,
        y=ordered_values,
        marker=dict(
            color=ordered_colors,
            colorscale='RdYlGn_r',
            showscale=False
        ),
        text=ordered_values,
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Distribuição da Escala DAFOR (Todos os Monitoramentos)",
        xaxis_title="Categoria DAFOR",
        yaxis_title="Frequência Absoluta",
        xaxis=dict(
            categoryorder='array',
            categoryarray=ordered_labels,
            tickangle=-45
        ),
        height=450,
        template='plotly_white'
    )
    
    return fig


def create_dafor_by_year_stacked_chart():
    """Create stacked bar chart showing DAFOR class distribution by year for REBIO + Entorno."""
    service = CoralDataService()
    
    # Get REBIO + Entorno locality IDs
    from cs_controllers import REBIO_ENTORNO_LOCALITIES
    
    # Get DAFOR data
    dafor_data = service.get_dafor_data(None, None)
    
    if dafor_data.empty:
        return go.Figure().update_layout(
            title="Sem dados DAFOR disponíveis",
            height=450
        )
    
    # Filter to REBIO + Entorno localities
    dafor_data = dafor_data[dafor_data['locality_id'].isin(REBIO_ENTORNO_LOCALITIES)]
    
    if dafor_data.empty:
        return go.Figure().update_layout(
            title="Sem dados DAFOR para REBIO + Entorno",
            height=450
        )
    
    # Parse dates and extract year
    dafor_data['date'] = pd.to_datetime(dafor_data['date'], dayfirst=True, errors='coerce')
    dafor_data = dafor_data.dropna(subset=['date'])
    dafor_data['year'] = dafor_data['date'].dt.year
    
    # Process DAFOR values (they may be comma-separated strings)
    if dafor_data['dafor_value'].apply(lambda x: isinstance(x, str) and ',' in str(x)).any():
        dafor_data['dafor_value'] = dafor_data['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        dafor_data = dafor_data.explode('dafor_value')
    
    dafor_data['dafor_value'] = pd.to_numeric(dafor_data['dafor_value'], errors='coerce')
    dafor_data = dafor_data.dropna(subset=['dafor_value'])
    
    # Filter valid DAFOR values (0, 2, 4, 6, 8, 10)
    dafor_data = dafor_data[dafor_data['dafor_value'].isin([0, 2, 4, 6, 8, 10])]
    
    # Count occurrences by year and DAFOR class
    yearly_counts = dafor_data.groupby(['year', 'dafor_value']).size().reset_index(name='count')
    
    # Create pivot table for easier plotting
    pivot_data = yearly_counts.pivot(index='year', columns='dafor_value', values='count').fillna(0)
    
    # DAFOR labels and colors
    dafor_labels = {
        0: 'Ausente (0)',
        2: 'Raro (2)',
        4: 'Ocasional (4)',
        6: 'Frequente (6)',
        8: 'Abundante (8)',
        10: 'Dominante (10)'
    }
    
    dafor_colors = {
        0: '#2ecc71',   # Green - Absent
        2: '#3498db',   # Blue - Rare
        4: '#f39c12',   # Orange - Occasional
        6: '#e67e22',   # Dark Orange - Frequent
        8: '#e74c3c',   # Red - Abundant
        10: '#c0392b'   # Dark Red - Dominant
    }
    
    fig = go.Figure()
    
    # Add a trace for each DAFOR class
    for dafor_value in [0, 2, 4, 6, 8, 10]:
        if dafor_value in pivot_data.columns:
            fig.add_trace(go.Bar(
                name=dafor_labels[dafor_value],
                x=pivot_data.index,
                y=pivot_data[dafor_value],
                marker_color=dafor_colors[dafor_value],
                text=pivot_data[dafor_value].astype(int),
                textposition='inside',
                textfont=dict(color='white')
            ))
    
    fig.update_layout(
        title="Distribuição de Classes DAFOR por Ano (REBIO Arvoredo + Entorno)",
        xaxis_title="Ano",
        yaxis_title="Número de Registros",
        barmode='stack',
        height=500,
        template='plotly_white',
        legend=dict(
            title="Classe DAFOR",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.15
        ),
        hovermode='x unified'
    )
    
    return fig


def create_dafor_sum_by_locality_chart():
    """Create stacked bar chart showing sum of DAFOR scores by locality."""
    service = CoralDataService()
    
    # Get sum of DAFOR values by locality
    dafor_sum_data = service.get_sum_of_dafor_by_locality(None, None)
    
    if dafor_sum_data.empty or dafor_sum_data["DAFOR"].dropna().empty:
        return go.Figure().update_layout(
            title="Sem dados DAFOR disponíveis",
            height=500
        )
    
    # DAFOR category mapping
    dafor_num_to_label = {
        10: "D", 8: "A", 6: "F", 4: "O", 2: "R"
    }
    category_order = [10, 8, 6, 4, 2]
    category_labels = [dafor_num_to_label[v] for v in category_order]
    
    # DAFOR full labels for legend
    dafor_full_labels = {
        10: "D - Dominante",
        8: "A - Abundante",
        6: "F - Frequente",
        4: "O - Ocasional",
        2: "R - Raro"
    }
    
    def map_to_category(val):
        return min(category_order, key=lambda x: abs(x - val))
    
    df = dafor_sum_data.copy()
    df = df[df["DAFOR"] > 0]  # Exclude Ausente and zero values
    df["DAFOR_CAT"] = df["DAFOR"].apply(map_to_category)
    df["DAFOR_CLASS"] = df["DAFOR_CAT"].map(dafor_num_to_label)
    
    df_grouped = df.groupby(['name', 'DAFOR_CLASS'], as_index=False)['DAFOR'].sum()
    
    pivot = df_grouped.pivot(index='name', columns='DAFOR_CLASS', values='DAFOR').fillna(0)
    
    for label in category_labels:
        if label not in pivot.columns:
            pivot[label] = 0
    
    pivot = pivot[category_labels]
    pivot["total"] = pivot.sum(axis=1)
    pivot = pivot[pivot["total"] > 0]  # Only localities with total > 0
    pivot = pivot.sort_values("total", ascending=False)
    
    # Create figure
    fig = go.Figure()
    
    # Color scheme for DAFOR categories
    colors = {
        'D': '#c0392b',   # Dark Red - Dominant
        'A': '#e74c3c',   # Red - Abundant
        'F': '#e67e22',   # Dark Orange - Frequent
        'O': '#f39c12',   # Orange - Occasional
        'R': '#3498db'    # Blue - Rare
    }
    
    # Add traces for each DAFOR category in reverse order
    for label in reversed(category_labels):
        if label in pivot.columns:
            fig.add_trace(go.Bar(
                name=dafor_full_labels[category_order[category_labels.index(label)]],
                y=pivot.index,
                x=pivot[label],
                orientation='h',
                marker_color=colors.get(label, '#999999'),
                text=pivot[label].astype(int),
                textposition='inside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>' + dafor_full_labels[category_order[category_labels.index(label)]] + ': %{x}<extra></extra>'
            ))
    
    fig.update_layout(
        title="Soma das Pontuações DAFOR por Localidade",
        xaxis_title="Soma da Pontuação DAFOR",
        yaxis_title="Localidade",
        barmode='stack',
        height=500,
        template='plotly_white',
        yaxis=dict(autorange="reversed"),
        legend=dict(
            title="Categoria DAFOR",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.15
        ),
        hovermode='y unified'
    )
    
    return fig


def create_removal_rate_per_day_chart():
    """Create chart showing coral mass removal rate per management day per year for REBIO + Entorno."""
    service = CoralDataService()
    
    # Get REBIO + Entorno locality IDs
    from cs_controllers import REBIO_ENTORNO_LOCALITIES
    
    # Get all management data
    management_data = service.get_management_data(None, None)
    
    if management_data.empty:
        return go.Figure().update_layout(
            title="Sem dados de manejo disponíveis",
            height=400
        )
    
    # Filter to REBIO + Entorno localities
    management_data = management_data[management_data['locality_id'].isin(REBIO_ENTORNO_LOCALITIES)]
    
    if management_data.empty:
        return go.Figure().update_layout(
            title="Sem dados de manejo para REBIO + Entorno",
            height=400
        )
    
    # Ensure date is datetime and extract year
    management_data['date'] = pd.to_datetime(management_data['date'], dayfirst=True, errors='coerce')
    management_data = management_data.dropna(subset=['date'])
    management_data['year'] = management_data['date'].dt.year
    management_data['date_only'] = management_data['date'].dt.date
    
    # Group by year and calculate metrics
    yearly_stats = management_data.groupby('year').agg({
        'managed_mass_kg': 'sum',  # Total mass per year
        'date_only': 'nunique',     # Number of unique management days
        'management_id': 'count'    # Total events (for reference)
    }).reset_index()
    
    yearly_stats.columns = ['year', 'total_mass_kg', 'unique_days', 'total_events']
    
    # Calculate removal rate: kg per management day
    yearly_stats['kg_per_day'] = yearly_stats['total_mass_kg'] / yearly_stats['unique_days']
    yearly_stats['kg_per_day'] = yearly_stats['kg_per_day'].round(2)
    
    # Create figure
    fig = go.Figure()
    
    # Bar chart for kg per day
    fig.add_trace(go.Bar(
        x=yearly_stats['year'],
        y=yearly_stats['kg_per_day'],
        name='kg/dia de manejo',
        marker_color='#2ecc71',
        text=yearly_stats['kg_per_day'].round(1),
        textposition='auto',
        textfont=dict(size=12, color='white'),
        hovertemplate=(
            '<b>Ano: %{x}</b><br>' +
            'Razão: %{y:.2f} kg/dia<br>' +
            '<extra></extra>'
        )
    ))
    
    # Find years with mechanical methods
    mechanical_years = management_data[
        management_data['method'].str.contains('mecanizado', case=False, na=False)
    ]['year'].unique()
    
    fig.update_layout(
        title="Razão de Remoção de Massa de Coral por Dia de Manejo por Ano<br><sub>REBIO Arvoredo + Entorno Imediato</sub>",
        xaxis=dict(
            title="Ano",
            dtick=1
        ),
        yaxis=dict(
            title="Massa Removida por Dia de Manejo (kg/dia)"
        ),
        height=500,
        template='plotly_white',
        hovermode='x unified',
        showlegend=False
    )
    
    # Add red arrows to indicate mechanical methods
    for year in mechanical_years:
        fig.add_annotation(
            x=year,
            y=1.05,
            yref='paper',
            text='',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='red',
            ax=0,
            ay=-30
        )
    
    return fig


def create_mass_per_cylinder_chart():
    """Create chart showing managed mass per cylinder by year for REBIO + Entorno."""
    service = CoralDataService()
    
    # Get REBIO + Entorno locality IDs
    from cs_controllers import REBIO_ENTORNO_LOCALITIES
    
    # Get all management data
    management_data = service.get_management_data(None, None)
    
    if management_data.empty:
        return go.Figure().update_layout(
            title="Sem dados de manejo disponíveis",
            height=400
        )
    
    # Filter to REBIO + Entorno localities
    management_data = management_data[management_data['locality_id'].isin(REBIO_ENTORNO_LOCALITIES)]
    
    if management_data.empty:
        return go.Figure().update_layout(
            title="Sem dados de manejo para REBIO + Entorno",
            height=400
        )
    
    # Ensure date is datetime and extract year
    management_data['date'] = pd.to_datetime(management_data['date'], dayfirst=True, errors='coerce')
    management_data = management_data.dropna(subset=['date'])
    management_data['year'] = management_data['date'].dt.year
    
    # Convert cylinders to numeric and filter out invalid/missing values
    management_data['number_of_cylinders'] = pd.to_numeric(management_data['number_of_cylinders'], errors='coerce')
    management_data['managed_mass_kg'] = pd.to_numeric(management_data['managed_mass_kg'], errors='coerce')
    
    # Filter out rows with zero or null cylinders/mass
    management_data = management_data[
        (management_data['number_of_cylinders'] > 0) & 
        (management_data['managed_mass_kg'] > 0)
    ]
    
    if management_data.empty:
        return go.Figure().update_layout(
            title="Sem dados válidos de cilindros para REBIO + Entorno",
            height=400
        )
    
    # Group by year and calculate metrics
    yearly_stats = management_data.groupby('year').agg({
        'managed_mass_kg': 'sum',
        'number_of_cylinders': 'sum'
    }).reset_index()
    
    # Calculate mass per cylinder
    yearly_stats['kg_per_cylinder'] = yearly_stats['managed_mass_kg'] / yearly_stats['number_of_cylinders']
    yearly_stats['kg_per_cylinder'] = yearly_stats['kg_per_cylinder'].round(2)
    
    # Create figure
    fig = go.Figure()
    
    # Bar chart for kg per cylinder
    fig.add_trace(go.Bar(
        x=yearly_stats['year'],
        y=yearly_stats['kg_per_cylinder'],
        name='kg/cilindro',
        marker_color='#3498db',
        text=yearly_stats['kg_per_cylinder'].round(2),
        textposition='auto',
        textfont=dict(size=12, color='white'),
        hovertemplate=(
            '<b>Ano: %{x}</b><br>' +
            'Massa por Cilindro: %{y:.2f} kg<br>' +
            'Total de Cilindros: %{customdata[0]}<br>' +
            'Massa Total: %{customdata[1]:.1f} kg<br>' +
            '<extra></extra>'
        ),
        customdata=yearly_stats[['number_of_cylinders', 'managed_mass_kg']].values
    ))
    
    # Find years with mechanical methods
    mechanical_years = management_data[
        management_data['method'].str.contains('mecanizado', case=False, na=False)
    ]['year'].unique()
    
    fig.update_layout(
        title="Massa Manejada por Cilindro Utilizado por Ano<br><sub>REBIO Arvoredo + Entorno Imediato</sub>",
        xaxis=dict(
            title="Ano",
            dtick=1
        ),
        yaxis=dict(
            title="Massa por Cilindro (kg/cilindro)"
        ),
        height=500,
        template='plotly_white',
        hovermode='x unified',
        showlegend=False
    )
    
    # Add red arrows to indicate mechanical methods
    for year in mechanical_years:
        fig.add_annotation(
            x=year,
            y=1.05,
            yref='paper',
            text='',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='red',
            ax=0,
            ay=-30
        )
    
    return fig


def get_report_layout():
    """Generate the real-time report layout with processed data and charts."""
    
    layout = dbc.Container([
        # Header
        html.H2("Relatório em Tempo Real", className="mb-2 mt-4"),
        html.P(
            "Análises detalhadas de todos os dados de monitoramento e manejo do coral-sol. "
            "Os dados são processados em tempo real a partir da base de dados completa do Banco de Dados específico para os monitoramentos do coral-sol do Instituto Hórus."
            "Este relatório apresenta uma visão abrangente da situação atual do coral-sol, incluindo estatísticas gerais, evolução temporal, distribuição de abundância e eficiência do manejo."
            "Caso deseje análises específicas por período ou localidade, utilize a aba 'Dashboard' para acessar filtros personalizados e gráficos interativos.",
            className="mb-4",
            style={"color": "#ffffff"}
        ),
        html.Hr(),
        
        # Summary Statistics Cards
        html.H3("Estatísticas Gerais", className="mt-4 mb-3"),
        create_summary_statistics(),
        
        # Temporal Evolution Section
        html.Hr(className="mt-5"),
        html.H3("Evolução Temporal", className="mb-3"),
        dcc.Markdown("""
        O gráfico abaixo mostra a evolução do esforço de monitoramento ao longo do tempo(numero de transectos visuais de 1 minuto) diferenciando transectos com detecção e sem detecção de coral-sol. 
        Os dados são agrupados por período (ano-mês) para mostrar tendências temporais na presença do coral-sol nos monitoramentos realizados.
        """),
        dcc.Loading(
            dcc.Graph(id='report-temporal-chart', figure=create_temporal_evolution_chart()),
            type="circle"
        ),
        
        # Occurrence Registration Section
        html.Hr(className="mt-5"),
        html.H3("Marcação de Ocorrências", className="mb-3"),
        dcc.Markdown("""
        Número de ocorrências de coral-sol registradas por ano. Cada ponto representa uma nova ocorrência 
        georreferenciada identificada durante atividades de monitoramento. Na aba 'Dashboard', é possível filtrar por localidade e período e visualizar as fotos das marcações.             
        """),
        dcc.Loading(
            dcc.Graph(id='report-occurrence-chart', figure=create_occurrence_by_year_chart()),
            type="circle"
        ),
        
        # Locality Ranking Section
        html.Hr(className="mt-5"),
        html.H3("Ranking de Localidades", className="mb-3"),
        dcc.Markdown("""
        Ranking das 15 localidades com maior DPUE (Detecções Por Unidade de Esforço),
        considerando todos os dados de monitoramento disponíveis.
        """),
        dcc.Loading(
            dcc.Graph(id='report-ranking-chart', figure=create_locality_ranking_chart()),
            type="circle"
        ),
        
        # DAFOR Distribution Section
        html.Hr(className="mt-5"),
        html.H3("Distribuição da Escala DAFOR", className="mb-3"),
        dcc.Markdown("""
        Distribuição de frequência das categorias da escala DAFOR em todos os monitoramentos.
        A escala DAFOR varia de 0 (Ausente) a 10 (Dominante), indicando a abundância do coral-sol.
        """),
        dcc.Loading(
            dcc.Graph(id='report-dafor-chart', figure=create_dafor_distribution_chart()),
            type="circle"
        ),
        
        # DAFOR by Year Stacked Section
        html.Hr(className="mt-5"),
        html.H3("Evolução das Classes DAFOR por Ano", className="mb-3"),
        dcc.Markdown("""
        Distribuição anual das classes DAFOR para as localidades da REBIO Arvoredo e Entorno Imediato.
        O gráfico empilhado mostra como a abundância do coral-sol varia ao longo dos anos.
        """),
        dcc.Loading(
            dcc.Graph(id='report-dafor-year-stacked', figure=create_dafor_by_year_stacked_chart()),
            type="circle"
        ),
        
        # DAFOR Sum by Locality Section
        html.Hr(className="mt-5"),
        html.H3("Soma de Pontuações DAFOR por Localidade", className="mb-3"),
        dcc.Markdown("""
        Soma das pontuações DAFOR agrupadas por localidade e categoria da escala DAFOR.
        Este gráfico apresenta um sumário da abundância do coral-sol em cada localidade monitorada,
        mostrando a distribuição das categorias de abundância acumuladas ao longo de todos os monitoramentos.
        Os dados devem ser interpretados com cautela, pois este produto não leva em consideração os esforços diferentes realizados em cada localidade.             
        """),
        dcc.Loading(
            dcc.Graph(id='report-dafor-sum-locality', figure=create_dafor_sum_by_locality_chart()),
            type="circle"
        ),
        
        # Management Efficiency Section
        html.Hr(className="mt-5"),
        html.H3("Esforço de Manejo", className="mb-3"),
        dcc.Markdown("""
        Análise da massa total manejada por ano e o número de eventos de manejo realizados. As setas vermelhas indicam anos em que métodos mecanizados foram utilizados, o que pode influenciar a eficiência do manejo.
        """),
        dcc.Loading(
            dcc.Graph(id='report-management-chart', figure=create_management_efficiency_chart()),
            type="circle"
        ),
        
        # Removal Rate per Day Section
        html.Hr(className="mt-5"),
        html.H3("Massa Manejada por dia por ano", className="mb-3"),
        dcc.Markdown("""
        Razão de remoção de massa de coral por dia de manejo ao longo dos anos.
        Este indicador mostra a massa manejada por dia de manejo, considerando apenas os dias
        em que houve atividades de remoção na REBIO Arvoredo e Entorno Imediato. As setas vermelhas indicam anos em que métodos mecanizados foram utilizados, o que pode influenciar a eficiência do manejo.
        """),
        dcc.Loading(
            dcc.Graph(id='report-removal-rate-chart', figure=create_removal_rate_per_day_chart()),
            type="circle"
        ),
        
        # Mass per Cylinder Section
        html.Hr(className="mt-5"),
        html.H3("Massa Manejada por Cilindro", className="mb-3"),
        dcc.Markdown("""
        Razão de massa de coral manejada por cilindro utilizado ao longo dos anos.
        Este indicador mostra a eficiência do manejo em relação ao consumo de ar por mergulhadores (Coelho-Souza et al., 2025),
        considerando apenas eventos com registro válido de cilindros na REBIO Arvoredo e Entorno Imediato. 
         As setas vermelhas indicam anos em que métodos mecanizados foram utilizados, o que pode influenciar a eficiência do manejo.
        """),
        dcc.Loading(
            dcc.Graph(id='report-mass-per-cylinder-chart', figure=create_mass_per_cylinder_chart()),
            type="circle"
        ),
        
        # Footer note
        html.Hr(className="mt-5"),
        html.P(
            "Nota: Todos os gráficos são gerados dinamicamente com base nos dados mais recentes da base de dados. "
            "Para análises específicas por período ou localidade, utilize a aba 'Dashboard'.",
            className="small mt-4 mb-5",
            style={"color": "#ffffff"}
        ),
        
    ], fluid=True)
    
    return layout
