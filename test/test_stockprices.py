# pylint: disable=C0111, E1101
"""Test StockPrices.
Run from the project folder:
`python -m unittest test.test_stockprices -v`

"""
import unittest
from datetime import datetime
from datetime import timedelta
from plot_stocks.data.stockprices import StockPrices


class TestStockPrices(unittest.TestCase):
    """Test cases for StockPrices."""
    def setUp(self):
        self.stockprices = StockPrices()

    def tearDown(self):
        self.stockprices = None

    def test_get_symbols(self):
        res = self.stockprices.get_symbols()
        self.assertGreater(len(res), 5000)

    def test_get_metadata(self):
        meta = self.stockprices.get_metadata(['AAPL', 'GOOGL'])
        self.assertEqual(meta.shape, (2, 6))
        self.assertIn('Apple Inc.', list(meta['name']))
        self.assertIn('Alphabet Inc.', list(meta['name']))


    def test_get_aapl_history(self):
        data = self.stockprices.get_history('AAPL')
        self.assertEqual(
            data.loc[('AAPL', '2017-01-02'), 'close'][0], 115.82)

    def test_get_aapl_recent_history(self):
        data = self.stockprices.get_history(
            ['AAPL'])
        day = datetime.today() - timedelta(1)
        # if a weekend subtract 2 days
        if day.weekday() > 5:
            day = day - timedelta(2)
        self.assertIn(
            day.strftime('%Y-%m-%d'), data.index.levels[1])

    def test_get_aapl_from_2018(self):
        data = self.stockprices.get_history(
            'AAPL', start_date='2018-1-1')
        self.assertEqual(
            data.index.levels[1][0].strftime('%Y-%m-%d'), '2018-01-01')

    def test_get_aapl_til_2018(self):
        data = self.stockprices.get_history(
            'AAPL', end_date='2017-12-29')
        self.assertEqual(
            data.index.levels[1][-1].strftime('%Y-%m-%d'), '2017-12-29')

    def test_get_appl_intraday(self):
        data = self.stockprices.get_intraday('AAPL')
        interval = min(data.reset_index()['date'].diff().dropna())
        self.assertEqual(15., interval.seconds/60.)

    def test_get_appl_intraday_1min(self):
        data = self.stockprices.get_intraday('AAPL', 1)
        interval = min(data.reset_index()['date'].diff().dropna())
        self.assertEqual(1, interval.seconds/60)

    def test_get_appl_googl_history(self):
        data = self.stockprices.get_history(['AAPL', 'GOOGL'])
        self.assertIn('AAPL', data.index.levels[0])
        self.assertIn('GOOGL', data.index.levels[0])

    def test_get_appl_googl_intraday(self):
        data = self.stockprices.get_intraday(['AAPL', 'GOOGL'])
        self.assertIn('AAPL', data.index.levels[0])
        self.assertIn('GOOGL', data.index.levels[0])

if __name__ == '__main__':
    unittest.main()
