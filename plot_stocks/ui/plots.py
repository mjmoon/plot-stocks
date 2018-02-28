"""This module provides functions for plotting."""
from plotly import graph_objs as go

def plot_history(data, names, start, end):
    """Plot figure."""
    traces = []
    layout = dict(
        xaxis=dict(range=[start, end]),
        showlegend=True
        )
    for (sym, dat), name in\
        zip(data.groupby(level=0), names):
        traces.append(
            go.Scatter(
                x=dat.index.levels[1],
                y=dat['close'],
                mode='lines',
                text=sym,
                name=name
            )
        )
    return dict(data=traces, layout=layout)
