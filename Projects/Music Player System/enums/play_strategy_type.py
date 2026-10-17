from enum import Enum


class PlayStrategyType(Enum):
    SEQUENTIAL = "SEQUENTIAL"
    RANDOM = "RANDOM"
    CUSTOM_QUEUE = "CUSTOM_QUEUE"