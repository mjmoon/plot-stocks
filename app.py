# pylint: disable=E1101, C0103
"""A dash application for plotting up-to-date stock prices."""
from datetime import date
from dateutil.relativedelta import relativedelta
import dash
from plot_stocks.data.stockprices import StockPrices
from plot_stocks import ui

app = dash.Dash()
stock = StockPrices()
symbols = stock.get_symbols()

app.layout = ui.layout(symbols)

@app.callback(
    dash.dependencies.Output('plot-stock', 'figure'),
    [dash.dependencies.Input('ticker-selector-dropdown', 'value')])
def update_figure(selected_symbols):
    """Update figure with inputs."""
    print('Tickers selected: ', selected_symbols)
    start_date = date.today() - relativedelta(years=5)
    tickerdata = stock.get_history(selected_symbols, start_date)
    names = list(stock.get_metadata(selected_symbols)['name'])

    return ui.plot_history(
        tickerdata, names, '2015-1-1', '2018-2-28'
    )

app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# Loading screen CSS
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server()
