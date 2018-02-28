# pylint: disable=E0611
"""This module defines the layout of the app."""
from dash_core_components import Dropdown, RadioItems, Graph
from dash_html_components import H3, Div

def _symbol_selector_dropdown(symbols, default='GOOGL'):
    """Return symbol selector."""
    return Dropdown(
        id='ticker-selector-dropdown',
        options=[
            {'label': sym, 'value': sym}
            for sym in symbols],
        value=default,
        multi=True)

def _period_selector_radio(periods):
    """Return period selector."""
    return RadioItems(
        options=[
            {'label': x[0], 'value': x[1]}
            for x in periods
        ],
        value=periods[0][1],
        labelStyle={'display': 'inline-block'}
    )


def layout(symbols):
    """Return the UI layout."""
    periods = [
        ('1 day', [1, 'd']),
        ('5 days', [5, 'd']),
        ('1 month', [1, 'm']),
        ('3 months', [3, 'm']),
        ('1 year', [1, 'y']),
        ('5 years', [5, 'y'])
        ]
    return Div([
        H3('Stock prices'),
        Div([
            Div([_symbol_selector_dropdown(symbols)],
                style={
                    'width': '45%',
                    'float': 'left',
                    'display': 'inline-block'
                }),
            Div([_period_selector_radio(periods)],
                style={
                    'width': '45%',
                    'float': 'right',
                    'display': 'inline-block'
                })
            ], style={'display': 'inline-block', 'width': '100%'}),
        Graph(id='plot-stock')
        ])
