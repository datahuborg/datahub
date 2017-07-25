import numpy as np

from scorpionsql.functions import *
from scorpionsql.errfunc import *


class AggErr(object):
    
    def __init__(self, agg, keys, npts, errtype, metadata={}):
        """
        @param npts either an int or a tuple (min, max)
        """
        self.agg = agg
        self.keys = keys
        self.npts = npts
        self.errtype = ErrTypes(errtype, None)
        self.erreq = metadata.get('erreq', None)
        self.metadata = metadata or {}

    def __str__(self):
        return str([str(self.agg), self.keys, self.npts, str(self.errtype), self.erreq])

    error_func = property(lambda self: self.__error_func__())
    

    def __error_func__(self):
        f = self.agg.func
        f.set_errtype(self.errtype)
        return f
        if self.agg.func == 'avg':
            return FastAvgErrFunc(self)
        if self.agg.func == 'stddev':
            return FastStdErrFunc(self)
        if self.agg.func == 'sum':
            return FastSumErrFunc(self)
        if self.agg.func == 'min':
            return MinErrFunc(self)
        if self.agg.func == 'corr':
            return FastCorrErrFunc(self)
        raise NotImplementedError

    def bad_error_funcs(self, keys=None):
      if keys is None:
        keys = self.keys
      if self.errtype.errtype == ErrTypes.EQUALTO:
        ret = []
        for eqv in self.erreq:
          ef = self.agg.func.clone()
          ef.set_errtype(ErrTypes(self.errtype.errtype, eqv))
          ret.append(ef)
        return ret
      return [self.error_func.clone() for key in keys]

    def good_error_funcs(self, keys=[]):
      ret = []
      for key in keys:
        ef = self.error_func.clone()
        ef.errtype.errtype = ErrTypes.EQUALTO
        ef.errtype.erreq = None
        ret.append(ef)
      return ret



