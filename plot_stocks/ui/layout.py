# pylint: disable=E0611
"""This module defines the layout of the app."""
from dateutil.relativedelta import relativedelta
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
        id='period-selector-radio',
        options=[
            {'label': x[0], 'value': x[1]}
            for x in periods
        ],
        value=0,
        labelStyle={'display': 'inline-block'}
    )


def layout(symbols):
    """Return the UI layout."""
    periods = [
        ('1 day', 0),
        ('1 week', 1),
        ('1 month', 2),
        ('3 months', 3),
        ('1 year', 4),
        ('5 years', 5)
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
        Graph(
            id='plot-stock',
            config={'displayModeBar': False}
            )
        ])

def get_periods():
    """Return a list of relativedelta objects."""
    return [
        relativedelta(),
        relativedelta(days=6),
        relativedelta(months=1),
        relativedelta(months=3),
        relativedelta(years=1),
        relativedelta(years=5)
        ]
