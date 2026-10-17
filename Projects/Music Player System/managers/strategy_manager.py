from strategies.sequential_play_strategy import SequentialPlayStrategy
from strategies.random_play_strategy import RandomPlayStrategy
from strategies.custom_queue_strategy import CustomQueueStrategy
from strategies.play_strategy import PlayStrategy

from enums.play_strategy_type import PlayStrategyType


class StrategyManager:
    _instance = None

    def __init__(self):
        self._sequential_strategy = SequentialPlayStrategy()
        self._random_strategy = RandomPlayStrategy()
        self._custom_queue_strategy = CustomQueueStrategy()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = StrategyManager()
        return cls._instance

    def get_strategy(self, strategy_type: PlayStrategyType) -> PlayStrategy:

        if strategy_type == PlayStrategyType.SEQUENTIAL:
            return self._sequential_strategy

        elif strategy_type == PlayStrategyType.RANDOM:
            return self._random_strategy

        else:
            return self._custom_queue_strategy