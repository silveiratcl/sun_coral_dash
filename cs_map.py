from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.colors
import json
from services.data_service import CoralDataService
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.cm


def value_to_color(val, vmin, vmax, cmap_name='viridis'):
    norm = (val - vmin) / (vmax - vmin) if vmax > vmin else 0
    cmap = matplotlib.cm.get_cmap(cmap_name)
    rgba = cmap(norm)
    return matplotlib.colors.rgb2hex(rgba)


def build_map_figure(dpue_df):
    """
    Builds a map figure for DPUE values using Plotly."""
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd
    import json

    service = CoralDataService()
    localities = service.get_locality_data()

    # Only keep localities present in the filtered dpue_df
    localities = localities[localities['locality_id'].isin(dpue_df['locality_id'])]
    localities = localities.merge(dpue_df[['locality_id', 'DPUE']], on='locality_id', how='left')
    localities['DPUE'] = localities['DPUE'].fillna(0)

    dpue_min = localities['DPUE'].min()
    dpue_max = localities['DPUE'].max()
    colorscale = 'Viridis'

    fig = go.Figure()
    for _, row in localities.iterrows():
        try:
            points = json.loads(row['coords_local'])
            if points and isinstance(points, list) and isinstance(points[0], list):
                lats, lons = zip(*points)
                color = value_to_color(row['DPUE'], dpue_min, dpue_max, 'viridis')
                fig.add_trace(go.Scattermapbox(
                    showlegend=False,
                    lat=lats,
                    lon=lons,
                    mode="lines+markers",
                    name="",
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
            lat=[None], lon=[None],
            mode="markers",
            marker=dict(
                size=0.1,
                color=np.linspace(dpue_min, dpue_max, 10),
                colorscale=colorscale,
                cmin=dpue_min,
                cmax=dpue_max,
                colorbar=dict(
                    title="DPUE",
                    thickness=25,
                    y=0.5,
                    x=1.02,
                    xanchor="left",
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
        mean_lat, mean_lon = -27, -48

    fig.update_layout(
        template="plotly_dark",
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": mean_lat, "lon": mean_lon},
        margin={"r":10,"t":30,"l":10,"b":10},
        height=600
    )
    return fig

def build_dafor_sum_map_figure(df_dafor_sum):
    """
    Builds a map figure for DAFOR sum values using Plotly."""

    service = CoralDataService()
    localities = service.get_locality_data()

    # Merge DAFOR sum into localities
    localities = localities[localities['locality_id'].isin(df_dafor_sum['locality_id'])]
    localities = localities.merge(df_dafor_sum[['locality_id', 'DAFOR']], on='locality_id', how='left')
    localities['DAFOR'] = localities['DAFOR'].fillna(0)

    dafor_min = localities['DAFOR'].min()
    dafor_max = localities['DAFOR'].max()
    colorscale = 'Viridis'

    fig = go.Figure()
    for _, row in localities.iterrows():
        try:
            points = json.loads(row['coords_local'])
            if points and isinstance(points, list) and isinstance(points[0], list):
                lats, lons = zip(*points)
                color = value_to_color(row['DAFOR'], dafor_min, dafor_max, 'viridis')
                fig.add_trace(go.Scattermapbox(
                    showlegend=False,
                    lat=lats,
                    lon=lons,
                    mode="lines+markers",
                    name="",
                    line=dict(width=6, color=color),
                    marker=dict(size=6, color=color),
                    hoverinfo="text",
                    text=f"{row['name']}<br>DAFOR: {row['DAFOR']:.2f}" if not pd.isna(row['DAFOR']) else row['name']
                ))
        except Exception as e:
            print(f"Error plotting {row['name']}: {e}")
            pass

    # Add a dummy trace for the colorbar
    dafor_vals = localities['DAFOR'].dropna()
    if not dafor_vals.empty:
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None],
            mode="markers",
            marker=dict(
                size=0.1,
                color=np.linspace(dafor_min, dafor_max, 10),
                colorscale=colorscale,
                cmin=dafor_min,
                cmax=dafor_max,
                colorbar=dict(
                    title="DAFOR",
                    thickness=25,
                    y=0.5,
                    x=1.02,
                    xanchor="left",
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
        mean_lat, mean_lon = -27, -48

    fig.update_layout(
        template="plotly_dark",
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": mean_lat, "lon": mean_lon},
        margin={"r":10,"t":30,"l":10,"b":10},
        height=600
    )
    return fig
    
def build_occurrence_map_figure(occurrences_df):
    """ Builds a map figure for occurrences using Plotly."""
   
    def parse_coords(coord):
        if isinstance(coord, str):
            try:
                coord = json.loads(coord)
            except Exception:
                return [None, None]
        if isinstance(coord, list) and len(coord) == 1 and isinstance(coord[0], list) and len(coord[0]) == 2:
            return coord[0]
        return [None, None]

    occurrences_df[['lat', 'lon']] = occurrences_df['spot_coords'].apply(lambda x: pd.Series(parse_coords(x)))
    print(occurrences_df[['spot_coords', 'lat', 'lon']].head())  # Debug

    # Build hover text with info and image links
    def make_hover(row):
        txt = (
            f"Localidade: {row.get('locality_id', '')}<br>"
            f"Data: {row.get('date', '')}<br>"
            f"Profundidade: {row.get('depth', '')}<br>"
            f"Acesso: {row.get('access', '')}<br>"
            f"Geomorfologia: {row.get('geomorphology', '')}<br>"
        )
        # Add image links if available
        if pd.notnull(row.get('subaquatica_photo')):
            txt += f"<a href='{row['subaquatica_photo']}' target='_blank'>Subaquática</a><br>"
        if pd.notnull(row.get('superficie_photo')):
            txt += f"<a href='{row['superficie_photo']}' target='_blank'>Superfície</a>"
        return txt

    occurrences_df['hover'] = occurrences_df.apply(make_hover, axis=1)

    fig = go.Figure(go.Scattermapbox(
        lat=occurrences_df['lat'],
        lon=occurrences_df['lon'],
        mode="markers",
        marker=dict(size=12, color='red', symbol='circle'),
        hoverinfo="text",
        text=occurrences_df['hover'],
        customdata=occurrences_df[['subaquatica_photo', 'superficie_photo']].values,
        showlegend=False,
    ))

    # Center map
    if not occurrences_df.empty:
        mean_lat = occurrences_df['lat'].mean()
        mean_lon = occurrences_df['lon'].mean()
    else:
        mean_lat, mean_lon = -27, -48

    fig.update_layout(
        template="plotly_dark",
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": mean_lat, "lon": mean_lon},
        margin={"r":10,"t":30,"l":10,"b":10},
        height=600
    )
    return fig

def parse_coords(coord_str):
    """Parse coordinates from a JSON string."""
    try:
        coord = json.loads(coord_str)
        if isinstance(coord, list) and len(coord) == 1 and isinstance(coord[0], list) and len(coord[0]) == 2:
            return coord[0]
    except Exception:
        pass
    return [None, None]



