import numpy as np

def square(
    tlist: list, 
    amplitude: float
) -> np.ndarray:
    return np.array([amplitude] * len(tlist))

def cos(
    tlist: np.ndarray,
    amplitude: float,
    a: float,
    b: float
) -> np.ndarray:
    """ cos pules

    amplitude * cos(ax+b)

    """
    _tlist = a * tlist + b
    return amplitude * np.cos(_tlist)

def sin(
    tlist: list,
    amplitude: float,
    a: float,
    b: float
) -> np.ndarray:
    """ sin pules

    amplitude * sin(ax+b)

    """
    _tlist = a * tlist + b
    return amplitude * np.sin(_tlist)

"""def super_gaussian(
    tlist: list=None, 
    param: list=None
) -> list:
    t_total = tlist[-1]
    t_middle = t_total / 2
    amp = param[0]
    tau = param[1]
    def _super_gaussian(t):
        t = t % t_total
        a = np.exp(- t_middle**2 / tau**2)
        return amp * (np.exp(-(t-t_middle)**2 / tau**2) - a) / (1-a) 
    return np.array(list(map(_super_gaussian, tlist)))
"""
