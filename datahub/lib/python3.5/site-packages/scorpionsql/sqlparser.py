import subprocess
import os
import json
import sys

from scorpionsql.errfunc import *
from scorpionsql.functions import *
from scorpionsql.sql import *

dirname = os.path.dirname(os.path.abspath( __file__ ))
classes = "%s/jars/scala-library.jar:%s/jars/sqlparser.jar" % (dirname, dirname)
__agg2f__ = {'avg' : AvgErrFunc,
             'std' : StdErrFunc,
             'stddev' : StdErrFunc, 
             'stddev_samp': StdErrFunc,
             'stddev_pop': StdErrFunc,
             'min' : MinErrFunc,
             'max' : MaxErrFunc,
             'sum' : SumErrFunc,
             'corr' : CorrErrFunc,
             'count' : CountErrFunc,
             'abs' : AbsErrFunc}

def parse_sql(q):
    return SqlParser()(q)

class SqlParser(object):
    def __init__(self):
        pass

    def __call__(self, q):
        jsonobj = self.fetch_json(q)
        if not jsonobj:
            raise "could not parse"

        queryobj = self.json_to_obj(jsonobj)
        return queryobj

    def fetch_json(self, q):
        try:
            cmd = ["java", "-cp", classes, "main", q]
            ret = subprocess.check_output(cmd)
            print ret
            return json.loads(ret)
        except subprocess.CalledProcessError as e:
            print >>sys.stderr, str(e)
            import traceback
            traceback.print_exc()
            return None


    def json_to_obj(self, j):
        select = j['select']
        fr = j['from']
        where = j['where']
        group = j['group']
        having = j['having']
        order = j['order']
        limit = j['limit']


        aggsels, normsels = [], []
        sels = []
        import pdb
        #pdb.set_trace()
        for sexpr, alias in select:
            cols = get_vars(sexpr)
            expr_str = expr_to_str(sexpr)

            if alias is None:
                if sexpr[0] == '_var_':
                    alias = sexpr[1]
                elif sexpr[0].strip('_') not in ('literal', 'cast', 'extract', '+', '-', '*', '/'):
                    alias = sexpr[0]
            
            if alias in group:
                sel = SelectExpr(alias, cols, expr_str, sexpr)
            else:
                func = construct_func_expr(sexpr)
                sel = SelectAgg(None, func, cols, expr_str, sexpr)
            sels.append(sel)

        order = ['%s %s' % (a,b) for a,b in map(tuple, order)]
        limit = limit[0] if limit else None

        return Query(None,
                     sels,
                     fr,
                     where,
                     group,
                     order,
                     limit)


def expr_to_str(n, l=None):
    """
    construct SQL string from expression node
    """
    op = n[0]
    if op.startswith('_') and op.endswith('_'):
        op = op.strip('_')
        if op == 'var':
            return n[1]
        elif op == 'literal':
            if isinstance(n[1], basestring):
                return "'%s'" % n[1]
            return str(n[1])
        elif op == 'cast':
            return "(%s)::%s" % (expr_to_str(n[1]), n[2])
    elif op in '+-*/':
        return "(%s) %s (%s)" % (expr_to_str(n[1]), op, expr_to_str(n[2]))
    elif op == "extract":
        return "extract( %s from %s )" % (n[1], expr_to_str(n[2]))
    else:
        arg = ','.join(map(expr_to_str, n[1:]))
        return "%s(%s)" % (op, arg)
    
def get_vars(n):
    """
    extract variables from expression node
    defined by tuple-pair: (_var_, [variable name])
    """
    op = n[0]
    if op.startswith('_') and op.endswith('_'):
        op = op.strip('_')
        if op == 'var':
            return [n[1]]
        return []
    else:
        ret = []
        for c in n[1:]:
            vs = get_vars(c)
            if vs:
                ret.extend(vs)
        return ret


def construct_func_expr(n):
    """
    construct the function expression 
    """
    op = n[0]
    if op.startswith('_') and op.endswith('_'):
        op = op.strip('_')
        if op == 'var':
            return Var(str(n[1]))
        elif op == 'literal':
            if isinstance(n[1], basestring):
                raise "not implemented"
            return Constant(n[1])
        elif op == 'cast':
            raise "not implemented"
    elif op in '+-/*':
        return ArithErrFunc(op, *map(construct_func_expr,n[1:]))
    else:
        klass = __agg2f__.get(op, None)
        if klass:
            return klass(map(construct_func_expr, n[1:]))
        raise "no klass"


if __name__ == '__main__':
    from tests.gentestdata import *
    for name in datasetnames:
        test_data = get_test_data(name)
        q = test_data[1]
        parser = SqlParser()
        qobj = parser(q)
        print qobj
    exit()
    import Orange
    t = Orange.data.Table('iris')
    names = ['slen', 'swid', 'plen', 'pwid', 'iris']
    for d, n in zip(t.domain, names):
        d.name = n

    func = qobj.select.aggregates[0].func
    func.setup(t, ErrTypes(ErrTypes.TOOHIGH))

    tn = t.to_numpy('a')[0]
    for i in xrange(len(t)):
        print func(tn[(i,),:], "rm"), tn[i,:]
        
    
