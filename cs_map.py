import plotly.express as px

def create_map(data):
    if data.empty or 'latitude' not in data.columns:
        return px.scatter_mapbox(lat=[], lon=[], height=500)
    
    return px.scatter_mapbox(
        data,
        lat='latitude',
        lon='longitude',
        hover_name='name',
        hover_data=['date', 'value'],
        zoom=10,
        height=500,
        mapbox_style="open-street-map"
    )