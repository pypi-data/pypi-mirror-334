STRATEGIES = {}
CHAINS = {}

def strategy(grouper):
    def decorator(cls):
        if grouper not in STRATEGIES:
            STRATEGIES[grouper] = []
        STRATEGIES[grouper].append(cls())
        return cls
    return decorator

def chain(grouper, order):
    def decorator(cls):
        if grouper not in CHAINS:
            CHAINS[grouper] = []
        CHAINS[grouper].append((order, cls()))
        CHAINS[grouper].sort(key=lambda x: x[0])
        return cls
    return decorator