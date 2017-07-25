import numpy as np
from scorpionsql.functions import *


def compute_bad_inf(bdelta, bcount, c):
  if bcount == 0:
    return 0
  return float(bdelta / pow(bcount, c))
compute_bad_inf = np.vectorize(compute_bad_inf)

def compute_bad_score(bds, bcs, c, smooth=0.025):
  bcs = np.array(bcs).astype(float)

  if not bds or not bcs.any():
    return c * -float('inf')

  topbots = zip(bds, bcs)
  binfs = [compute_bad_inf(top, bot, c) for top, bot in topbots]
  binfs = np.array(binfs)

  bcs[bcs > 0] = 1
  bcs[bcs <= 0] = smooth
  weights = bcs / bcs.sum()
  try:
    return np.average(binfs, axis=0, weights=weights)
  except:
    print bcs
    print weights
    print bds
    import traceback
    traceback.print_exc()
    import pdb
    pdb.set_trace()

def compute_influence(l, binf, ginf, nclauses=0, *args):
  return l * binf - (1. - l) * ginf - 0.0001 * nclauses # XXX: add - len(rule.clauses)


class ErrTypes(object):
    WRONG = 0
    EQUALTO = 1
    TOOHIGH = 2
    TOOLOW = 3

    def __init__(self, errtype, erreq=None):
        try:
            self.errtype = errtype.errtype
        except:
            self.errtype = errtype
        self.erreq = erreq            
        #if self.errtype == ErrTypes.EQUALTO and erreq is None:
        #    raise "Error Type EQUALTO needs a value"

    def __str__(self):
        return '%d\t%s' % (self.errtype, self.erreq)

    @staticmethod
    def valid(err):
        return err >= 0 and err <= 3

    def __call__(self, oldv, newv):
      if self.errtype == ErrTypes.TOOHIGH:
          return oldv - newv
      if self.errtype == ErrTypes.TOOLOW:
          return newv - oldv
      if self.errtype == ErrTypes.EQUALTO:
        diff = abs(self.erreq - newv)
        olddiff = abs(self.erreq - oldv)
        return 1. - (1.+diff)/(1.+olddiff)
      return abs(newv - oldv)

    def clone(self):
        return ErrTypes(self.errtype, erreq=self.erreq)

def setup_wrapper(f):
    def h(self, table):
        ret = f(self, table)
        if self.errtype.errtype == ErrTypes.EQUALTO:
          if self.errtype.erreq is None:
            self.errtype.erreq = ret
        return ret
    return h

class BaseErrFunc(object):
    """
    Function is
    initialized with child nodes

    __call__(data) passes data to child nodes
    """
    def __init__(self):
        self.ncalls = 0
        self.errtype = None
        self.data = None
        self.parent = None
        self.children = []

    is_root = property(lambda self: self.parent == None)

    def clone(self):
        pass

    def set_errtype(self, errtype):
        if errtype:
            self.errtype = errtype.clone()

    def setup(self, table):
        self.domain = table.domain
        self.data = table

    def state(self, data):
        raise RuntimeError("not implemented")

    def update(self, states, num=1):
        raise RuntimeError("not implemented")

    def remove(self, big_state, state, n=1):
        raise RuntimeError("not implemented")

    def recover(self, state):
        raise RuntimeError("not implemented")

    def __call__(self, data, opt):
        pass

    def distribution(self, table, k=0.05):
        k = max(len(table) * k, min(len(table), 10))
        sampler = Orange.data.sample.SubsetIndices2(p0=len(table) - k)
        sampler.random_generator = Orange.misc.Random(len(table))

        scores = []
        for i in xrange(50):
            idxs = sampler(table)
            sample = table.select_ref(idxs).to_numpyMA('ac')[0]
            score = self(sample, "rm") / k
            scores.append( score )

        return np.mean(scores), np.std(scores)    
    

class AggErrFunc(BaseErrFunc):
    def __init__(self, children, klass):
        BaseErrFunc.__init__(self)

        self.klass = klass
        self.f = klass()
        self.fempty = klass()
        self.children = children
        for c in children:
            c.parent = self

    def clone(self):
        newchildren = [c.clone() for c in self.children]
        ret = type(self)(newchildren)
        ret.set_errtype(self.errtype)
        return ret

    def set_errtype(self, errtype):
        BaseErrFunc.set_errtype(self, errtype)
        map(lambda c: c.set_errtype(errtype), self.children)
        return self

    @setup_wrapper
    def setup(self, table):
        BaseErrFunc.setup(self, table)
        domain = table.domain
        vals = map(lambda c: c.setup(table), self.children)
        self.f(*vals)
        self.value = self.f.value()
        return self.value

    def state(self, data):
        vals = map(lambda c: c(data, 'scratch'), self.children)
        return self.f.state(*vals)

    def update(self, states, num=1):
        return self.f.update(states, num=num)

    def remove(self, big_state, state, n=1):
        return self.f.remove(big_state, state, n)

    def recover(self, state):
        "recompute the actual value, then compare it against the truth"
        newval = self.f.recover(state)
        return self.errtype(self.value, newval)


    def __call__(self, data, mode='rm'):
        self.ncalls += 1
        vals = map(lambda c: c(data, mode), self.children)
        if mode == 'rm':
            newval = self.f.delta(rm=vals)
        if mode == 'scratch':
            newval = self.fempty.delta(add=vals)

        if self.is_root:
            return self.errtype(self.value, newval)
        else:
            return newval


class CorrErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, LinearFit)

    @setup_wrapper
    def setup(self, table):
        BaseErrFunc.setup(self, table)
        domain = table.domain
        vals = map(lambda c: c.setup(table), self.children)
        self.f(*vals)
        self.value = self.f.corr()
        return self.value

    def __call__(self, data, mode='rm'):
        self.ncalls += 1
        vals = map(lambda c: c(data, mode), self.children)
        if mode == 'rm':
            newval = self.f.corr(rm=vals)
        if mode == 'scratch':
            newval = self.fempty.corr(add=vals)

        if self.is_root:
            return self.errtype(self.value, newval)
        return newval

        

class StdErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, StdFunc)

class AvgErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, AvgFunc)

class MinErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, MinFunc)

class MaxErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, MaxFunc)

class SumErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, SumFunc)

class CountErrFunc(AggErrFunc):
    def __init__(self, children):
        AggErrFunc.__init__(self, children, CountFunc)


def _add(a,b):
    return a + b
def _sub(a,b):
    return a - b
def _mul(a,b):
    return a / b
def _div(a,b):
    return a / b


class ArithErrFunc(BaseErrFunc):
    op2f = {'+' : _add,
            '-' : _sub,
            '*' : _mul,
            '/' : _div}

    def __init__(self, op, left, right):
        BaseErrFunc.__init__(self)
        self.op = op
        self.l = left
        self.r = right
        self.f = ArithErrFunc.op2f[op]
        self.l.parent = self
        self.r.parent = self

    def clone(self):
        ret = ArithErrFunc(self.op, self.l.clone(), self.r.clone())
        ret.set_errtype(self.errtype)
        return ret

    def set_errtype(self, errtype):
        BaseErrFunc.set_errtype(self, errtype)
        map(lambda c: c.set_errtype(errtype), [self.l, self.r])

    @setup_wrapper
    def setup(self, table):
        BaseErrFunc.setup(self, table)
        domain = table.domain
        self.lval = self.l.setup(table)
        self.rval = self.r.setup(table)
        self.value = self.f(self.lval, self.rval)
        return self.value

    def __call__(self, data, mode='rm'):
        self.ncalls += 1
        vals = map(lambda c: c(data, mode), [self.l, self.r])
        newval = self.f(*vals)

        if self.is_root:
            return self.errtype(self.value, newval)
        return newval

class AbsErrFunc(BaseErrFunc):
    def __init__(self, children):
        BaseErrFunc.__init__(self)
        self.child = children[0] if isinstance(children, list) else children
        self.child.parent = self

    def clone(self):
        ret = AbsErrFunc(self.child.clone())
        ret.set_errtype(self.errtype)
        return ret

    @setup_wrapper
    def setup(self, table):
        v = abs(self.child.setup(table))
        self.value = v
        return v

    def __call__(self, data, mode='rm'):
        self.ncalls += 1
        newval = abs(self.child(data, mode))
        
        if self.is_root:
            return self.errtype(self.value, newval)
        return newval

    


class Constant(BaseErrFunc):
    def __init__(self, v):
        BaseErrFunc.__init__(self)        
        self.v = v

    def clone(self):
        return self

    @setup_wrapper
    def setup(self, table):
        return self.v
        return np.array([self.v] * len(table))

    def __call__(self, data_array, mode='rm'):
        self.ncalls += 1
        return self.v
        return np.array([self.v] * data_array.shape[0])

class Var(BaseErrFunc):
    def __init__(self, var):
        BaseErrFunc.__init__(self)
        self.var = var
        self.idx = None

    def clone(self):
        return self

    def setup(self, table):
        domain = table.domain
        self.idx = domain.index(domain[self.var])
        return self(table.to_numpyMA('ac')[0])
    
    def __call__(self, data_array, mode='rm'):
        self.ncalls += 1
        if isinstance(data_array, np.ndarray):
            if len(data_array.shape) == 1:
                return data_array[self.idx]
            return data_array[:, self.idx]
        return np.array([float(row[self.idx].value) for row in data_array])

class DummyVar(BaseErrFunc):
    def __call__(self):
        BaseErrFunc.__init__(self)

    def clone(self):
        return self

    def setup(self, data):
        return np.array(sum(data) )

    def __call__(self, data_array, mode='rm'):
        return np.array(data_array)



if __name__ == '__main__':
    ef = AvgErrFunc([DummyVar()])
    s1 = ef.state(range(10))
    s2 = ef.state(range(4))
    print ef.recover(s1), np.mean(range(10))
    print ef.recover(s2), np.mean(range(4))
    print ef.recover(ef.update(s1, s2)), np.mean(range(10) + range(4))
    print ef.recover(ef.remove(s1, s2)), np.mean(range(4,10))
