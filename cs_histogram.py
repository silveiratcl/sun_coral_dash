import plotly.express as px

def create_histogram(data=None, indicators=None):
    """Create histogram visualization of selected indicators"""
    if data is None or len(data) == 0:
        return px.bar(title="No data available")
    
    # Default to showing abundance if available
    column = 'abundance' if 'abundance' in data.columns else data.columns[0]
    
    fig = px.histogram(
        data,
        x=column,
        nbins=20,
        title=f"Distribution of {column.capitalize()}",
        height=400
    )
    
    fig.update_layout(
        bargap=0.1,
        xaxis_title=column.capitalize(),
        yaxis_title="Count"
    )
    
    return fig