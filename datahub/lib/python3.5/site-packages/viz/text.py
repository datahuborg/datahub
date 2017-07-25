import math


def format_float(x, max_width):
    '''format_float will ensure that a number's decimal part is truncated to
    fit within some bounds, unless the whole part is wider than max_width,
    which is a problem you need to sort out yourself.
    '''
    # width of (whole part + 1 (to avoid zero)) + 1 because int floors, not ceils
    whole_width = int(math.log10(abs(x) + 1)) + 1
    # for +/- sign
    sign_width = 1 if x < 0 else 0
    # for . if we show it
    decimal_point_width = 1 if max_width >= whole_width else 0
    return '%.*f' % (max_width - whole_width - sign_width - decimal_point_width, x)


def float_reader(lines):
    for line in lines:
        if not line.isspace():
            yield float(line)
