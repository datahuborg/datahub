import numpy as np


def total(xs):
    print sum(xs)


def normalize(xs):
    '''
    Restrict xs into the interval (0, 1) via a linear transformation
    as long as len(xs) > 1, 0 and 1 will be elements of the resulting array
    '''
    x_min, x_max = np.min(xs), np.max(xs)
    return (xs - x_min) / (x_max - x_min)


def quantiles(xs, qs=None, step=25):
    if qs is None:
        qs = range(0, 100 + step, step)
    return zip(qs, np.percentile(xs, qs))
