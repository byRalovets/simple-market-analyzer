import unittest
import requests
from unittest.mock import MagicMock, patch

from util.symbols import Symbols

from const.url import URL


class SymbolsTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_exchange_info = {
            "symbols": [
                {"symbol": "BTCUSDT"},
                {"symbol": "ETHUSDT"},
                {"symbol": "BNBUSDT"},
                {"symbol": "BTCBUSD"},
                {"symbol": "ETHBUSD"},
            ]
        }

    # @patch.object(requests, 'get')
    def test_is_usdt_symbol(self):
        self.assertTrue(Symbols.is_usdt_symbol("BTCUSDT"))
        self.assertFalse(Symbols.is_usdt_symbol("BTCBUSD"))
        self.assertFalse(Symbols.is_usdt_symbol("ETHBTC"))

    def test_filter_usdt_symbols(self):
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "BTCBUSD", "ETHBUSD", "ETHBTC"]
        filtered_symbols = Symbols.filter_usdt_symbols(symbols)
        expected_result = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        self.assertEqual(filtered_symbols, expected_result)

    @patch.object(requests, 'get')
    def test_extract_symbols(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_exchange_info
        mock_get.return_value = mock_response

        symbols = Symbols.extract_symbols()

        self.assertEqual(len(symbols), 5)
        self.assertEqual(symbols, ["BTCUSDT", "ETHUSDT", "BNBUSDT", "BTCBUSD", "ETHBUSD"])
        mock_get.assert_called_once_with(URL.EXCHANGE_INFO_URL)

    @patch.object(requests, 'get')
    def test_extract_symbol_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"symbol": "BTCUSDT", "price": "50000"}
        mock_get.return_value = mock_response

        symbol_info = Symbols.extract_symbol_info("BTCUSDT")

        self.assertEqual(symbol_info["symbol"], "BTCUSDT")
        self.assertEqual(symbol_info["price"], "50000")
        mock_get.assert_called_once_with(URL.SYMBOL_STATS_URL, params={"symbol": "BTCUSDT"})

    @patch.object(requests, 'get')
    def test_extract_symbol_info_with_rate_limiting(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {
            "Retry-After": "5",
        }
        mock_get.return_value = mock_response

        with self.assertRaises(AssertionError):
            Symbols.extract_symbol_info("BTCUSDT")

        mock_get.assert_called_once_with(URL.SYMBOL_STATS_URL, params={"symbol": "BTCUSDT"})
        self.assertEqual(mock_response.json.call_count, 0)
        self.assertEqual(mock_response.json.call_count, 0)
        self.assertEqual(mock_response.status_code, 429)

    @patch.object(requests, 'get')
    def test_extract_symbol_info_with_unknown_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(AssertionError):
            Symbols.extract_symbol_info("BTCUSDT")

        mock_get.assert_called_once_with(URL.SYMBOL_STATS_URL, params={"symbol": "BTCUSDT"})
        self.assertEqual(mock_response.json.call_count, 0)
        self.assertEqual(mock_response.json.call_count, 0)
        self.assertEqual(mock_response.status_code, 500)

    def test_extract_symbol_info_empty_symbol(self):
        with self.assertRaises(KeyError):
            Symbols.extract_symbol_info("")

    def test_extract_symbol_info_invalid_symbol(self):
        with self.assertRaises(AssertionError):
            Symbols.extract_symbol_info("INVALID")


if __name__ == '__main__':
    unittest.main()
