# pylint: disable=E1101, C0103
"""A dash application for plotting up-to-date stock prices."""
from datetime import date
from dateutil.relativedelta import relativedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
from plotly import graph_objs as go
from plot_stocks.data.stockprices import StockPrices

stock = StockPrices()
symbols = stock.get_symbols()
app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock price tracker'),
    html.Div([
        html.Div(
            [dcc.Dropdown(
                id='ticker-selector-dropdown',
                options=[
                    {'label': sym, 'value': sym}
                    for sym in symbols],
                value='AAPL',
                multi=True)],
            style={
                'width': '48%',
                'float': 'left',
                'display': 'inline-block'
            }
        ),
        html.Div(
            [dcc.RadioItems(
                options=[
                    {'label': '1 day', 'value': 1},
                    {'label': '3 days', 'value': 3},
                    {'label': '1 month', 'value': 10},
                    {'label': '3 months', 'value': 30},
                    {'label': '6 months', 'value': 60},
                    {'label': '1 year', 'value': 100},
                    {'label': '5 year', 'value': 500}
                ],
                value=1,
                labelStyle={'display': 'inline-block'})],
            style={
                'width': '48%',
                'float': 'right',
                'display': 'inline-block'
            }
        )
    ], style={'display': 'inline-block', 'width': '100%'}),

    dcc.Graph(
        id='plot-stock',
        figure={'layout': dict(
            xaxis=dict(
                title='Date',
                range=['2016-01-01', '2018-02-28']
            )
        )}
    )])

@app.callback(
    dash.dependencies.Output('plot-stock', 'figure'),
    [dash.dependencies.Input('ticker-selector-dropdown', 'value')])
def update_figure(selected_symbols):
    """Update figure with inputs."""
    print('Tickers selected: ', selected_symbols)
    start_date = date.today() - relativedelta(years=5)
    tickerdata = stock.get_history(selected_symbols, start_date)
    names = list(stock.get_metadata(selected_symbols)['name'])
    traces = []
    for (sym, data), name in\
        zip(tickerdata.groupby(level=0), names):
        traces.append(
            go.Scatter(
                x=data.index.levels[1],
                y=data['open'],
                mode='lines',
                text=sym,
                name=name
            )
        )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1}
            )
    }

app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# Loading screen CSS
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server()
