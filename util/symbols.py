import time
import requests

from const.url import URL


class Symbols:

    @staticmethod
    def is_usdt_symbol(symbol: str) -> bool:
        if symbol.endswith("USDT"):
            return True
        return False

    @staticmethod
    def filter_usdt_symbols(symbols: list) -> list:
        return list(filter(Symbols.is_usdt_symbol, symbols))

    @staticmethod
    def extract_symbols() -> list:
        response = requests.get(URL.EXCHANGE_INFO_URL)
        exchange_info = response.json()
        return [symbol["symbol"] for symbol in exchange_info["symbols"]]

    @staticmethod
    def extract_symbol_info(symbol: str) -> object:
        if symbol is None or symbol == "":
            raise KeyError(f"symbol is {symbol}")

        params = {"symbol": symbol}
        response = requests.get(URL.SYMBOL_STATS_URL, params=params)

        if response.status_code == 429:
            # used_weight_1m = response.headers.get("x-mbx-used-weight-1m")
            retry_after_seconds = int(response.headers.get("Retry-After")) + 1

            print(f"request weight limit has been reached. wait {retry_after_seconds} seconds")
            time.sleep(retry_after_seconds)

        assert response.status_code == 200
        return response.json()
