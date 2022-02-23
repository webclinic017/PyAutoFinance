import backtrader as bt
import datetime as dt
import numpy as np

from pyautofinance.common.engine.Engine import Engine
from pyautofinance.common.options import EngineOptions, MarketOptions, TimeOptions, FeedOptions, BrokerOptions,\
    TimeFrame, Market, WritingOptions
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.usable_strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.sizers.SizersFactory import SizersFactory
from pyautofinance.common.feeds.FeedTitle import FeedTitle
from pyautofinance.common.analyzers.AnalyzersFactory import AnalyzersFactory
from pyautofinance.common.ResultsAnalyzer import ResultsAnalyzer

market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.h4, dt.datetime(2022, 1, 1))
feed_options = FeedOptions(market_options, time_options)

broker_options = BrokerOptions(100_000, 0.2)

strategy = StrategiesFactory().make_strategy(TestBracketStrategy, logging=False, stop_loss=2, risk_reward=range(2, 5))
sizer = SizersFactory().make_sizer(bt.sizers.PercentSizer, percents=10)
analyzer = AnalyzersFactory().make_analyzer(bt.analyzers.TradeAnalyzer)

writing_options = WritingOptions(candles_destination=FeedTitle(feed_options).get_pathname())

engine_options = EngineOptions(broker_options, feed_options, [strategy], sizer, analyzers=[analyzer],
                               writing_options=writing_options)

engine = Engine(engine_options)
results = engine.run()

results_analyzer = ResultsAnalyzer(results)

print(results_analyzer.pretty_pnls())
