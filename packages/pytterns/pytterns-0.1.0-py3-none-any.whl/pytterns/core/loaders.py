import inspect
from pytterns.core.decorators import STRATEGIES, CHAINS

class StrategyLoader:
    def __init__(self, name):
        self.name = name
        if name not in STRATEGIES:
            raise ValueError(f"No strategy found for strategy: {name}")

    def __getattr__(self, filter_method):
        """Allows you to call any method as a filter"""
        def filter_strategy(*args, **kwargs):
            for strategy in STRATEGIES[self.name]:
                methods = [name for name, func in inspect.getmembers(strategy, predicate=inspect.ismethod)
                    if not name.startswith("__")]
                method = getattr(strategy, filter_method, None)
                if callable(method):
                    if len(methods) == 1:
                        return method(*args, **kwargs)
                    if method(*args, **kwargs):
                        return strategy
            raise ValueError(f"No strategy in '{self.name}' passed the '{filter_method}' filter")
        return filter_strategy

class ChainLoader:
    def __init__(self, name):
        self.name = name
        if name not in CHAINS:
            raise ValueError(f"No chain found for: {name}")
        # Gets the already ordered handlers
        self.handlers = [handler for _, handler in CHAINS[name]]

    def handle(self, *args, **kwargs):
        for handler in self.handlers:
            method = getattr(handler, "handle", None)
            if callable(method):
                method(*args, **kwargs)
            else:
                raise TypeError(f"Class '{handler.__class__.__name__}' does not have the 'handle' method.")
