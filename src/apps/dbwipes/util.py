#
# this file has no deps on Scorpion
#
import re
import json
import decimal

from scorpionsql.errfunc import (
    AbsErrFunc, AvgErrFunc, CorrErrFunc, CountErrFunc, MaxErrFunc,
    MinErrFunc, StdErrFunc, SumErrFunc, Var)
from scorpionsql.sql import Query, Select, SelectAgg, SelectExpr


# JSON Encoder
class SummaryEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, float):
            if o == float('inf'):
                return 1e100
            elif o == float('-inf'):
                return -1e100

        if isinstance(o, decimal.Decimal):
            return float(o)

        if hasattr(o, 'isoformat'):
            s = o.isoformat()
            if not s.endswith("Z"):
                s += 'Z'
            return s
        return super(SummaryEncoder, self).default(o)


def where_to_sql(where_json, negate=False):
    is_type = lambda s, types: any([t in s for t in types])
    l = []
    args = []
    for clause_json in where_json:
        if 'sql' in clause_json:
            l.append(clause_json['sql'])
            continue

        ctype = clause_json['type']
        col = clause_json['col']
        vals = clause_json['vals']

        if not vals:
            continue

        if is_type(ctype, ['num', 'int', 'float', 'double', 'date', 'time']):
            q = "%%s <= %s and %s <= %%s" % (col, col)
            args.extend(vals)
        else:
            tmp = []
            vals = list(vals)
            if None in vals:
                tmp.append("(%s is null)" % col)

            realvals = list(filter(lambda v: v is not None, vals))
            if len(realvals) == 1:
                tmp.append("(%s = %%s)" % col)
                args.append(realvals[0])
            elif len(realvals):
                tmp.append("(%s in %%s)" % col)
                args.append(tuple(list(realvals)))
            q = ' or '.join(tmp)

        l.append(q)

    q = ' and '.join(filter(bool, l))
    if negate and q:
        q = "not(%s)" % q
    return q, args


__agg2f__ = {
    'avg': AvgErrFunc,
    'std': StdErrFunc,
    'stddev': StdErrFunc,
    'stddev_samp': StdErrFunc,
    'stddev_pop': StdErrFunc,
    'min': MinErrFunc,
    'max': MaxErrFunc,
    'sum': SumErrFunc,
    'corr': CorrErrFunc,
    'count': CountErrFunc,
    'abs': AbsErrFunc
}


def parse_agg(s):
    """
    parse an aggregation SELECT clause e.g., avg(temp) as foo
    into dictionary of function name, column, and alias components
    """
    # print(s)
    p = re.compile(
        '(?P<func>\w+)\(\s*(?P<col>[\w\,\s]+)\s*\)\s*(as\s+(?P<alias>\w+))?')
    d = p.match(s).groupdict()
    klass = __agg2f__[d['func'].strip()]
    expr = str(d['col'])
    cols = [col.strip() for col in expr.split(',')]
    varlist = [Var(col) for col in cols]
    # print(klass)
    # print(cols)
    # print(varlist)
    func = klass(varlist)
    return {
        'fname': d['func'],
        'func': func,
        'cols': cols,
        'alias': d.get('alias', '') or d['func']
    }


def expr_from_nonagg(s):
    """
    remove alias component of a nonaggregation SELECT clause
    """
    if ' as ' in s:
        return ' as '.join(s.split(' as ')[:-1])
    return s


def create_sql_obj(db, qjson):
    x = qjson['x']
    ys = qjson['ys']
    # sql = qjson['query']
    # dbname = qjson['db']
    table = qjson['table']
    negate = qjson.get('negate', False)
    where_json = qjson.get('where', []) or []
    basewheres_json = qjson.get('basewheres', []) or []

    where, args = where_to_sql(where_json, negate)
    basewheres, baseargs = where_to_sql(basewheres_json, False)
    where = ' and '.join(filter(bool, [where, basewheres]))
    args.extend(baseargs)

    select = Select()
    nonagg = SelectExpr(x['alias'], [x['col']], x['expr'], x['col'])
    select.append(nonagg)
    for y in ys:
        d = parse_agg(y['expr'])
        agg = SelectAgg(
            y['alias'], d['func'], d['cols'], y['expr'], d['cols'][0])
        select.append(agg)

    parsed = Query(
        db,
        select,
        [table],
        [where],
        [x['expr']],
        [expr_from_nonagg(x['expr'])]
    )

    return parsed, args


def pick(iterable, key):
    return [item[key] for item in iterable]
