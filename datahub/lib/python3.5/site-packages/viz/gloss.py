from viz import terminal


def gloss(alignments, prefixes=None, postfixes=None, width=None, toksep=' ', linesep='\n', groupsep='\n'):
    '''
    Creates an interlinear gloss (for pairs of tokens/types, POS-tags, labels, etc.)

    Take a list of [('a', 'DET'), ('beluga', 'N')] and return a string covering multiples lines, like:
        a   beluga
        DET N
    each item in `alignments` should have the same length, N
    `prefixes`, if provided, should be N-long
    `postfixes`, if provided, should be N-long
    '''
    if width is None:
        width = terminal.width()
    toksep_len = len(toksep)

    # a "group" is a N-line string, each line of which is at most `width` characters
    # `groups` is a list of such groups
    groups = []

    def flush_buffer(line_buffer):
        if len(line_buffer) > 0:
            lines = [toksep.join(tokens) for tokens in line_buffer]
            if prefixes:
                lines = [prefix + line for prefix, line in zip(prefixes, lines)]
            if postfixes:
                lines = [line + postfix for postfix, line in zip(postfixes, lines)]
            groups.append(linesep.join(lines))
        return [[] for _ in alignments[0]]

    # the line_buffer is an N-long list of lists of tokens (strings)
    # [[e1, e2, e3], [f1, f2, f3], [g1, g2, g3]]
    line_buffer = flush_buffer([])
    # the line_buffer_width is just the cumulative width of the current line_buffer
    line_buffer_width = 0

    for aligned in alignments:
        aligned = map(unicode, aligned)
        length = max(map(len, aligned))
        line_buffer_width += toksep_len + length
        if line_buffer_width >= width:
            line_buffer = flush_buffer(line_buffer)
            line_buffer_width = length
        for i, token in enumerate(aligned):
            line_buffer[i].append(token.ljust(length))

    flush_buffer(line_buffer)

    return groupsep.join(groups)
