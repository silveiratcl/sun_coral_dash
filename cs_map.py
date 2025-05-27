import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point

def create_map(data=None, center=None, indicators=None):
    """Create the main map visualization"""
    if data is None or len(data) == 0:
        return px.scatter_mapbox(lat=[], lon=[])
    
    # Convert to GeoDataFrame if not already
    if not isinstance(data, gpd.GeoDataFrame):
        gdf = gpd.GeoDataFrame(data)
    else:
        gdf = data
    
    # Create the base map
    fig = px.scatter_mapbox(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name="name",
        hover_data=["date", "locality_id"],
        zoom=10,
        height=600
    )
    
    # Update layout
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(center=center)
    )
    
    return fig