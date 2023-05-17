from util.symbols import Symbols


def main():
    print("application started")

    all_symbols = Symbols.extract_symbols()
    usdt_symbols = Symbols.filter_usdt_symbols(all_symbols)

    i = 0
    size = len(usdt_symbols)
    for symbol in usdt_symbols:
        symbol_info = Symbols.extract_symbol_info(symbol)
        print(f"[{++i}/{size}] stats for symbol {symbol} was received")


if __name__ == '__main__':
    main()
