import time
import ccxt

from backtrader.feeds import PandasData
from abc import ABC, abstractmethod
from ccxtbt import CCXTStore

from pyautofinance.common.options import Market
from pyautofinance.common.feeds.ccxt_utils import format_symbol_for_ccxt
from pyautofinance.common.broker.brokers import CCXTLiveBroker


class DatafeedGeneratorsFactory:

    @staticmethod
    def generate_datafeed(candles, feed_options, broker_options):
        time_options = feed_options.time_options
        market_options = feed_options.market_options

        if not time_options.end_date:  # No end date means we're looking for a live datafeed

            if market_options.market == Market.CRYPTO:
                return CryptoLiveDatafeedGenerator().generate_datafeed(feed_options, broker_options)

        return BacktestingDatafeedGenerator().generate_datafeed(candles, feed_options)


class DatafeedGenerator(ABC):

    @abstractmethod
    def generate_datafeed(self):
        pass


class BacktestingDatafeedGenerator(DatafeedGenerator):

    def generate_datafeed(self, candles, feed_options):
        time_options = feed_options.time_options
        timeframe = time_options.timeframe

        return PandasData(dataname=candles, timeframe=timeframe.bt_timeframe, compression=timeframe.bt_compression, datetime=0)


class CryptoLiveDatafeedGenerator(DatafeedGenerator):

    def generate_datafeed(self, feed_options, broker_options):
        market_options = feed_options.market_options
        time_options = feed_options.time_options

        symbol = market_options.symbol
        formatted_symbol = format_symbol_for_ccxt(symbol)

        timeframe = time_options.timeframe

        start_date = time_options.start_date

        broker = CCXTLiveBroker(broker_options)
        store = broker.get_store()
        return store.getdata(dataname=formatted_symbol, name=formatted_symbol, timeframe=timeframe.bt_timeframe,
                             fromdate=start_date, compression=timeframe.bt_compression, ohlcv_limit=99999,
                             sessionstart=start_date)
