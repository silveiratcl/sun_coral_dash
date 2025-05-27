import plotly.express as px

def create_histogram(data):
    """Simplest possible histogram function"""
    if data.empty:
        return px.bar()  # Empty histogram if no data
        
    return px.histogram(
        data,
        x='value',  # Change this to your actual column name
        nbins=10,
        height=400
    )