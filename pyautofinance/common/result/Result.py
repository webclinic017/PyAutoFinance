from pyautofinance.common.result.StratResult import StratResult
from pyautofinance.common.collections import StratsCollection


class Result:

    def __init__(self, engine_result, metrics_to_use):
        self.engine_result = engine_result
        self.metrics_to_use = metrics_to_use
        self.collections = self._build_strats_collections()
        self.symbols = self._build_symbols()

    def __getitem__(self, item):
        return self.collections[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.engine_result):
            symbol = list(self.engine_result.keys())[self.index]
            collection = self.collections[symbol]

            self.index += 1
            return symbol, collection
        else:
            raise StopIteration

    def __contains__(self, item):
        return item in self.collections

    def __setitem__(self, key, value):
        self.collections[key] = value

    def __add__(self, other):
        engine_result1 = self.engine_result
        engine_result2 = other.engine_result
        metrics_to_use = self.metrics_to_use

        engine_result3 = engine_result1.copy()
        engine_result3.update(engine_result2)

        return Result(engine_result3, metrics_to_use)

    def __iadd__(self, other):
        return self + other

    def _build_strats_collections(self):
        collections = {}
        for symbol, result in self.engine_result.items():
            strats_list = []
            for strat in result:
                for optimized_strat in strat:
                    strat_result = StratResult(optimized_strat, self.metrics_to_use)
                    strats_list.append(strat_result)
            collections[symbol] = StratsCollection(strats_list)
        return collections

    def _build_symbols(self):
        return [symbol for symbol in self.engine_result.keys()]

    def get_best_params(self, metric):
        best_params_per_symbol = {}
        for symbol, strats_collection in self.collections.items():
            sorted_strats_collection = strats_collection.sort_by_metric(metric)
            best_strat = sorted_strats_collection[0]
            best_params = dict(best_strat.params)
            best_params_per_symbol[symbol] = best_params
        return best_params_per_symbol

