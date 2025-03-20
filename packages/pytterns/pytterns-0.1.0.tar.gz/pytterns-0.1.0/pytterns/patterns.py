from pytterns.core.loaders import StrategyLoader, ChainLoader

class load:
    @staticmethod
    def strategy(grouper):
        return StrategyLoader(grouper)
    
    @staticmethod
    def chain(grouper):
        return ChainLoader(grouper)
