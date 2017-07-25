import sys
import argparse
from viz.geom import hist, points
from viz.stats import total
from viz.text import float_reader

types = dict(hist=hist, points=points, total=total)


def main():
    # print 'running example ...'
    # import scipy.stats
    # draws = scipy.stats.norm.rvs(size=1000, loc=-100, scale=10)
    # hist(draws, margin=10)
    parser = argparse.ArgumentParser(description='viz: data visualization in the terminal',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=argparse.FileType('r'), nargs='?', default=sys.stdin,
        help='File / stream of numbers')
    parser.add_argument('type', choices=types, help='Type of visualization to produce')
    opts = parser.parse_args()

    # float_reader is a generator, but numpy requires an actual list...
    xs = list(float_reader(opts.input))
    types[opts.type](xs)


if __name__ == '__main__':
    main()
