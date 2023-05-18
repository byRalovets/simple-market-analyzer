import matplotlib.pyplot as plt
import pandas as pd

from const.dataset import Dataset
from const.images import Images


def draw_pie(values, labels, name: str, bbox_to_anchor=None) -> None:
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.5f%%')
    plt.legend(loc='best', bbox_to_anchor=bbox_to_anchor)
    full_name = Images.FOLDER + name + Images.SVG_EXT
    plt.savefig(full_name, format=Images.SVG_FORMAT, dpi=1200, bbox_inches="tight")


def draw_bars(values, labels, name: str, colors=None, x_label: str = 'x', y_label: str = 'y',
              title: str = 'untitled') -> None:
    fig, ax = plt.subplots()
    if colors is None:
        plt.bar(labels, values)
    else:
        plt.bar(labels, values, color=colors)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation='vertical')
    full_name = Images.FOLDER + name + Images.SVG_EXT
    plt.savefig(full_name, format=Images.SVG_FORMAT, dpi=1200, bbox_inches="tight")
    plt.close(fig)


def analyze_market_activity(df: pd.DataFrame) -> None:
    labels = ['Торгуется', 'Не торгуется']
    values = [df[df['lastId'] > 0]['symbol'].count(), df[df['lastId'] == -1]['symbol'].count()]
    draw_pie(values, labels, 'activity-percent')


def drop_inactive_instruments(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(df[df['lastId'] == -1].index)


def analyze_greatest_prices(df: pd.DataFrame) -> None:
    instruments = df.nlargest(10, 'lastPrice').sort_values(by='lastPrice', ascending=True)
    symbols = instruments['symbol']
    prices = instruments['lastPrice']
    draw_bars(prices, symbols, '10-greatest-price', x_label='Инструмент', y_label='цена',
              title='Самые дорогие инструменты')


def analyze_greatest_volumes(df: pd.DataFrame) -> None:
    total_volume = df['quoteVolume'].sum()
    instruments = df.nlargest(10, 'quoteVolume').sort_values(by='quoteVolume', ascending=True)
    symbols = instruments['symbol']
    percents = instruments['quoteVolume'] / total_volume
    draw_pie(percents, symbols, '10-greatest-volume', bbox_to_anchor=(1.15, 1))


def analyze_greatest_volatility(df: pd.DataFrame) -> None:
    instruments = df
    instruments['priceChangePercentAbs'] = instruments['priceChangePercent'].abs()
    instruments = instruments.nlargest(10, 'priceChangePercentAbs').sort_values(by='priceChangePercentAbs',
                                                                                ascending=True)
    symbols = instruments['symbol']
    percents = instruments['priceChangePercentAbs']
    colors = ['g' if percent >= 0 else 'r' for percent in instruments['priceChangePercent']]
    draw_bars(percents, symbols, '10-greatest-volatility', colors, 'Инструмент',
              'Процент изменения цены', 'Самые волатильные инструменты')


def analyze_greatest_gap(df: pd.DataFrame) -> None:
    instruments = df
    instruments['abs_gap_percent'] = abs(instruments['askPrice'] - instruments['bidPrice']) / instruments['lastPrice']
    instruments = instruments.nlargest(10, 'abs_gap_percent').sort_values(by='abs_gap_percent', ascending=True)
    symbols = instruments['symbol']
    percents = instruments['abs_gap_percent']
    draw_bars(percents, symbols, '10-greatest-gap', x_label='Инструмент', y_label='Процент разницы ask/bid',
              title='Инструменты с наибольшим процентным разрывом между куплей/продажей')


df = pd.read_csv(Dataset.PATH)

analyze_market_activity(df)

drop_inactive_instruments(df)

analyze_greatest_prices(df)
analyze_greatest_volumes(df)
analyze_greatest_volatility(df)
analyze_greatest_gap(df)
