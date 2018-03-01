"""This module provides functions for plotting."""
from plotly import graph_objs as go

def plot_history(data, names):
    """Plot figure."""
    traces = []
    layout = dict(
        yaxis=dict(separatethousands=True),
        margin=dict(l=40, b=40, t=40, r=40),
        showlegend=True
        )
    for (sym, dat), name in\
        zip(data.groupby(level=0), names):
        traces.append(
            go.Scatter(
                x=dat.index.get_level_values(1),
                y=dat['close'],
                text=sym,
                name=name
            )
        )
    return dict(data=traces, layout=layout)
