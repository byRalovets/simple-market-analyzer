import json
import redis
import os

from const.database import Database
from util.symbols import Symbols


def main():
    print("application started")
    redis_client = redis.Redis(host=Database.REDIS_HOST,
                               port=Database.REDIS_PORT,
                               db=Database.REDIS_DB,
                               password=os.environ[Database.REDIS_PASSWORD_VAR_NAME],
                               charset=Database.REDIS_CHARSET,
                               decode_responses=True)
    print("redis connected")

    all_symbols = Symbols.extract_symbols()
    usdt_symbols = Symbols.filter_usdt_symbols(all_symbols)

    i = 0
    size = len(usdt_symbols)
    for symbol in usdt_symbols:
        symbol_info = Symbols.extract_symbol_info(symbol)
        redis_client.hset(Database.REDIS_HASH_NAME, symbol, json.dumps(symbol_info))

        print(f"[{++i}/{size}] stats for symbol {symbol} was persisted"
              f" to redis database ({Database.REDIS_HASH_NAME}/{symbol})")


if __name__ == '__main__':
    main()
