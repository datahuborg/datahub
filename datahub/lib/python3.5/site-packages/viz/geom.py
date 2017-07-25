from viz import terminal
from viz.text import format_float
from viz.stats import normalize
import numpy as np


def format_number_line(cells, left, right, margin=0):
    return '%s[%s]%s' % (
        format_float(left, margin).rjust(margin),
        u''.join(cells),
        format_float(right, margin).ljust(margin))


def hist(xs, range=None, margin=10, width=None):
    '''
    xs: array of numbers, preferably an np.array, can contain nans, infinities
    range: (minimum, maximum) tuple of numbers (defaults to (min, max) of xs)
    margin: number of characters to use for the min-max labels (default: 10)
    width: number of characters that will fit in a row (defaults to your terminal width)

    Example:

    >>> import scipy.stats
    >>> draws = scipy.stats.norm.rvs(size=100, loc=100, scale=10)
    >>> hist(draws, margin=5)
    '''
    if width is None:
        width = terminal.width()

    # add 1 to each margin for the [ and ] brackets
    n_bins = width - (2 * (margin + 1))
    # wrap it up as an array so we can index into it with a bool array. most likely it'll be a numpy array already
    xs = np.array(xs)
    finite = np.isfinite(xs)
    # don't copy it unless we need to (we don't need to if there are only finite numbers)
    # but if there are some nans / infinities, remove them
    finite_xs = xs[finite]  # if nonfinite.any() else xs
    # compute the histogram values as floats, which is easier, even though we renormalize anyway
    hist_values, bin_edges = np.histogram(finite_xs, bins=n_bins, density=True, range=range)
    # we want the highest hist_height to be 1.0
    hist_heights = hist_values / max(hist_values)
    # np.array(...).astype(int) will floor each value, if we wanted
    hist_chars = (hist_heights * (len(terminal.bars) - 1)).astype(int)
    cells = [terminal.bars[hist_char] for hist_char in hist_chars]

    print format_number_line(cells, bin_edges[0], bin_edges[-1], margin=margin)
    if not finite.all():
        # if we took any out, report it:
        nonfinite_xs = xs[~finite]
        neginf = np.isneginf(nonfinite_xs)
        nan = np.isnan(nonfinite_xs)
        posinf = np.isposinf(nonfinite_xs)
        print '%s %s %s' % (
            ('(%d) -inf' % np.count_nonzero(neginf) if neginf.any() else '').rjust(margin),
            ('(%d) nan' % np.count_nonzero(nan) if nan.any() else '').center(len(cells)),
            ('(%d) +inf' % np.count_nonzero(posinf) if posinf.any() else '').ljust(margin)
        )


def points(ys, width=None):
    '''Usage:
    import scipy.stats
    def walk(steps, position=0):
        for step in steps:
            position += step
            yield position
    positions = list(walk(scipy.stats.norm.rvs(size=1000)))
    points(positions)
    '''
    if width is None:
        width = terminal.width()

    ys = np.array(ys)
    n = len(ys)
    y_min, y_max = np.min(ys), np.max(ys)
    n_bins = min(width, n)
    bins_per_n = float(n_bins) / float(n)
    # print n, n_bins, n_per_bin, bins_per_n
    sums = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i, y in enumerate(ys):
        bin = int(i * bins_per_n)
        sums[bin] += y
        counts[bin] += 1
    bin_means = sums / counts
    # we want the lowest bin_height to be 0.0, and highest bin_height to be 1.0
    bin_heights = normalize(bin_means)
    bin_chars = (bin_heights * (len(terminal.bars) - 1)).astype(int)
    # print sums, counts, bin_means
    cells = [terminal.bars[bin_char] for bin_char in bin_chars]
    print '[%+f]' % y_max
    print u''.join(cells)
    print '[%+f]' % y_min
