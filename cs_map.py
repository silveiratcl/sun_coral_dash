from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.colors
import json
from services.data_service import CoralDataService
import pandas as pd
import numpy as np


def build_map_figure(selected_localities=None):
    service = CoralDataService()
    localities = service.get_locality_data()
    dpue_df = service.get_dpue_by_locality()
    print("Localities:", localities.shape)
    print("DPUE:", dpue_df.shape)

    # Merge DPUE into localities
    localities = localities.merge(dpue_df[['locality_id', 'DPUE']], on='locality_id', how='left')
    print("Merged:", localities.shape)
    print(localities[['locality_id', 'name', 'DPUE']].head())

    # For localities with no DPUE, set a default color or marker
    localities['DPUE'] = localities['DPUE'].fillna(0)  # or np.nan, as you prefer

    # Filter by selected_localities if provided
    if selected_localities and 0 not in selected_localities:
        localities = localities[localities['locality_id'].isin(selected_localities)]

    # Prepare color scale
    dpue_min = localities['DPUE'].min()
    dpue_max = localities['DPUE'].max()
    colorscale = plotly.colors.sequential.Viridis
   
    def dpue_to_color(dpue):
        if pd.isna(dpue):
            return 'gray'
        norm = (dpue - dpue_min) / (dpue_max - dpue_min) if dpue_max > dpue_min else 0
        idx = int(norm * (len(colorscale) - 1))
        return colorscale[idx]

    fig = go.Figure()
    for _, row in localities.iterrows():
        print(f"Plotting: {row['name']} DPUE={row['DPUE']}")
        try:
            points = json.loads(row['coords_local'])
            if points and isinstance(points, list) and isinstance(points[0], list):
                lats, lons = zip(*points)
                color = dpue_to_color(row['DPUE'])
                fig.add_trace(go.Scattermapbox(
                    showlegend=False,  # Hide legend for each locality
                    lat=lats,
                    lon=lons,
                    mode="lines+markers",
                    name="",  # No legend entry
                    line=dict(width=4, color=color),
                    marker=dict(size=6, color=color),
                    hoverinfo="text",
                    text=f"{row['name']}<br>DPUE: {row['DPUE']:.2f}" if not pd.isna(row['DPUE']) else row['name']
                ))
        except Exception as e:
            print(f"Error plotting {row['name']}: {e}")
            pass

    # Add a dummy trace for the colorbar
    dpue_vals = localities['DPUE'].dropna()
    if not dpue_vals.empty:
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None],  # invisible
            mode="markers",
            marker=dict(
                size=0.1,
                color=np.linspace(dpue_min, dpue_max, len(colorscale)),
                colorscale=colorscale,
                cmin=dpue_min,
                cmax=dpue_max,
                colorbar=dict(
                    title="DPUE",
                    thickness=25,
                    y=0.5,  # Center colorbar vertically
                    x=1.02,           # Move colorbar further right (outside plot area)
                    xanchor="left",   # Anchor to the left of the colorbar
                    yanchor="middle",
                    len=0.95
                ),
            ),
            showlegend=False,
            hoverinfo='none'
        ))

    if not localities.empty:
        mean_lat = localities['LATITUDE'].mean()
        mean_lon = localities['LONGITUDE'].mean()
    else:
        mean_lat, mean_lon = -27, -48  # fallback

    fig.update_layout(
        template="plotly_dark",
        mapbox_style="open-street-map",
        mapbox_zoom=8,
        mapbox_center={"lat": mean_lat, "lon": mean_lon},
        margin={"r":10,"t":30,"l":10,"b":10},
        height=600
    )    
    return fig

#dcc.Graph(id="cs-map-graph" )