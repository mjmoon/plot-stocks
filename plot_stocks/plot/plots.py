"""This module provides functions for plotting."""
from plotly import graph_objs as go

def lineplot(data, ylab='close'):
    """Return a plotly lineplot object."""
    return go.Scatter(
        x=data['date'],
        y=data[ylab],
        mode='lines',
        name='lines')
