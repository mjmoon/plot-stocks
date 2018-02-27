# pylint: disable=E1101
"""This module provides a class for getting stock prices."""
import re
import yaml
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pandas_datareader import data as web

class StockPrices(object):
    """Get up-to-date stock price data."""

    def __init__(self):
        self._datareader = web
        with open('_access.yml', 'r') as config:
            api_key = yaml.load(config)['AV_API_KEY']
        self._alphavantage = TimeSeries(
            api_key, output_format='pandas')
        self._iex_symbols = self._datareader.get_iex_symbols()

    def get_symbols(self):
        """Get available symbols from IEX."""
        return self._iex_symbols['symbol']

    def get_metadata(self, symbols):
        """Get metadat from IEX."""
        if isinstance(symbols, str):
            symbols = [symbols]
        return self._iex_symbols[self._iex_symbols['symbol'].isin(symbols)]

    def get_history(self, symbols,
                    start_date=None, end_date=None):
        """Get daily stock prices."""
        data = self._datareader.DataReader(
            symbols, 'morningstar', start_date, end_date)
        data.rename(columns=lambda x: x.lower(), inplace=True)
        data.index.names = [x.lower() for x in data.index.names]
        data = data.sort_index()
        return data

    def get_intraday(self, symbols,
                     interval=15, output_size='full'):
        """Get intra-day stock prices using Alpha Vantage API."""
        data_list = []
        if isinstance(symbols, str):
            symbols = [symbols]
        for sym in symbols:
            datum = self._alphavantage.get_intraday(
                sym,
                str(interval)+'min',
                output_size)[0]
            datum['symbol'] = sym
            data_list.append(datum)
        data = pd.concat(data_list)
        data.rename(
            columns=lambda x: re.sub(r'[^a-zA-Z_]', '', x),
            inplace=True)

        data.index = pd.to_datetime(data.index)
        data = data.reset_index().set_index(['symbol', 'date'])
        data = data.sort_index()
        return data
