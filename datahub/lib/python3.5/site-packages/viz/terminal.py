import os
import subprocess


# I'm not sure why my font in iterm doesn't like \u2588, but it looks weird.
#   It's too short and not the right width.
bars = u' \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2589'


def width(mechanism='tput'):
    if mechanism == 'stty':
        stty_size = os.popen('stty size', 'r').read()
        rows, columns = map(int, stty_size.split())
    else:
        tput_cols = subprocess.check_output(['tput', 'cols'])
        columns = int(tput_cols)
    return columns
