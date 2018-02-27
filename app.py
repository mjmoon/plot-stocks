"""A dash application for plotting up-to-date stock prices."""
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from plotly import graph_objs as go
from plot_stocks.data.stockprices import StockPrices

# Top ETFs
# https://www.investopedia.com/articles/etfs/top-etfs-long-term-investments/

def main():
    """Main function."""
    stock = StockPrices()
    symbols = stock.get_symbols()

    dropdown_opts = pd.DataFrame(
        data=dict(
            label=symbols,
            value=symbols
            )
        )

    _selected_etf = 'VOO'
    data = stock.get_history(
        _selected_etf, '2018-1-1', get_realtime=True)
    data.sort_index(inplace=True)

    app = dash.Dash()
    app.css.append_css(
        {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
    app.layout = html.Div([
        html.H1('Stock price tracker'),
        dcc.Dropdown(
            options=dropdown_opts.to_dict('records'),
            value=_selected_etf,
            multi=True
        ),
        dcc.RadioItems(
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
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id='example-plot',
            figure={
                'data': [
                    go.Scatter(
                        x=data.index,
                        y=data['open'],
                        # high=data['high'],
                        # low=data['low'],
                        # close=data['close'],
                        mode='lines',
                        text=data['symbol'],
                        opacity=0.8
                        )
                    ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Price'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1}
                    )
                }
            )
        ])

    app.run_server()


if __name__ == '__main__':
    main()
