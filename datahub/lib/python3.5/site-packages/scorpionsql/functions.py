import math
import numpy as np
from itertools import repeat

NAN = float('NaN')

class Func(object):
    def __init__(self, data=None):
        pass

    def state(self, data):
        pass

    def update(self, states, num=1):
        pass

    def remove(self, big_state, state, num=1):
        pass

    def recover(self, state):
        pass

    def __call__(self, data):
        pass

    def value(self):
        pass
    
    def delta(self, add=None, rm=None, update=False):
        pass

class CompositeFunc(object):
    def __init__(self, children, f, data=None):
        """
        @param children the aggregate functions that are composed together
        @param f output of children -> single value
        """
        self.children = children
        self.f = f

        if data:
            self(data)

    def value(self):
        return self.f(*map(lambda c: c.value(), self.children))

    def __call__(self, data):
        if data:
            map(lambda c: c(data), self.children)
        return self.value()

    def delta(self, **kwargs):
        return self.f(*map(lambda c: c.delta(**kwargs), self.children))

class StdFunc(Func):
    def __init__(self, data=None):
        self.x2 = 0.
        self.n = 0.
        self.mean = 0.
        self.std = 0.
        if data is not None:
            self(data)

    def state(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        x2 = np.dot(data, data)
        n = len(data)
        total = data.sum()

        return (x2, total, n)


    def update(self, states, num=1):
        x2s, totals, counts = zip(*states)
        x2 = sum(x2s)
        count = sum(counts)
        total = sum(totals)
        return (x2*num, total*num, count*num)
    
    def remove(self, bstate, state, num=1):
        x2, total, n = tuple(bstate)
        x2p, tp, np = self.update((state,))
        return (x2-(num*x2p), total-(num*tp), n-(num*np))
   
    def recover(self, state):
        x,t,n = tuple(state)
        top = (n*x - t**2)
        bot = n*n
        if top < -1e-9 or bot == 0:
            return NAN
        return math.sqrt(top/bot)


    def value(self):
        return self.std
        
    def __call__(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        self.x2 = np.dot(data, data)
        self.n = len(data)
        self.mean = np.mean(data)
        self.std = np.std(data)

    def delta(self, add=None, rm=None, update=False):
        add = add[0] if add else add
        rm = rm[0] if rm else rm
        #add = add.reshape(add.shape[0]) if add is not None and len(add.shape)==2 else add
        #rm = rm.reshape(rm.shape[0]) if rm is not None and len(rm.shape)==2 else rm

        x2, n, mean, std = self.x2, self.n, self.mean, self.std
        total = mean * n
        if add is not None:
            x2 += np.dot(add, add)
            total += add.sum()
            n += len(add)            
        if rm is not None:
            x2 -= np.dot(rm, rm)
            total -= rm.sum()
            n -= len(rm)
        top = (n*x2 - total**2)
        bot = n*n
        if top < -1e-9:
            top = 0.
        if bot == 0 or top < 0:
            return NAN
        std = math.sqrt( top / bot )

        if update:
            self.x2 = x2
            self.n = n
            self.mean = total / n
            self.std = std
        
        return std

class AvgFunc(Func):
    def __init__(self, data=None):
        self.n = 0.
        self.total = 0.
        if data is not None:
            self(data)

    def value(self):
        return self.total / self.n

    def state(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        return (np.mean(data), len(data))

    def update(self, states, num=1):
        totals, counts = zip(*states)
        totaln = float(sum(counts))
        newavg = sum([t * count / totaln for t,count in zip(totals, counts)])
        return (newavg, num*totaln)

    def remove(self, bstate, state, num=1.):
        t, count = tuple(bstate)
        rmt, rmcount = self.update((state,), num=num)
        newcount = float(count - rmcount)
        if newcount == 0:
            return (0, 0)
        newt = t*count / newcount - rmt*rmcount / newcount 
        return (newt, newcount)

    def recover(self, state):
        t,n = tuple(state)
        if not n:
            return NAN
        return t 

    def __call__(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        self.total = data.sum()
        self.n = len(data)

    def delta(self, add=None, rm=None, update=False):
        add = add[0] if add else add
        rm = rm[0] if rm else rm
        #add = add.reshape(add.shape[0]) if add is not None and len(add.shape)==2 else add
        #rm = rm.reshape(rm.shape[0]) if rm is not None and len(rm.shape)==2 else rm

        total, n = self.total, self.n
        if add is not None:
            total += add.sum()
            n += len(add)
        if rm is not None:
            total -= rm.sum()
            n -= len(rm)
        if n == 0:
            return 0
            #return NAN

        if update:
            self.total = total
            self.n = n
        
        return total / float(n)


class MinFunc(Func):
    def __init__(self, data=None):
        self.min = None
        if data is not None:
            self(data)        

    def value(self):
        return self.min

    def __call__(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        self.min = min(data)

    def delta(self, add=None, rm=None, update=False):
        ret = self.min
        if add is not None:
            ret = min(ret, min(add))
        if rm is not None:
            raise
        if update:
            self.min = ret
        return ret

class MaxFunc(Func):
    def __init__(self, data=None):
        self.max = None
        if data is not None:
            self(data)        

    def value(self):
        return self.max

    def __call__(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        self.max = max(data)

    def delta(self, add=None, rm=None, update=False):
        ret = self.max
        if add is not None:
            ret = max(ret, max(add))
        if rm is not None:
            raise

        if update:
            self.max = ret
        return ret


class SumFunc(Func):
    def __init__(self, data=None):
        self.total = 0.
        if data is not None:
            self(data)        

    def value(self):
        return self.total



    def state(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        return (data.sum(), len(data))

    def update(self, states, num=1):
        sums, counts = zip(*states)
        return (sum(sums) * num, sum(counts) * num)

    def remove(self, bstate, state, num=1):
        return (bstate[0] - num*state[0], bstate[1]-state[1])

    def recover(self, state):
        return state[0]

    def __call__(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        self.total += data.sum()

    def delta(self, add=None, rm=None, update=False):
        ret = self.total
        if add is not None:
            ret += sum(el.sum() for el in add)
        if rm is not None:
            ret -= sum(el.sum() for el in rm)

        if update:
            self.total = ret
        return ret



class CountFunc(Func):
    def __init__(self, data=None):
        self.total = 0.
        if data is not None:
            self(data)        

    def value(self):
        return self.total

    def state(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        return (len(data), )

    def update(self, states, num=1.):
        return (sum(s[0] for s in states) * num)

    def remove(self, bstate, state, num=1):
        return (bstate[0] - num*state[0],)

    def recover(self, state):
        return state[0]


    def __call__(self, data):
        if len(data.shape) == 2:
            data = data.reshape(data.shape[0])
        self.total = len(data)

    def delta(self, add=None, rm=None, update=False):
        ret = self.total
        if add is not None:
            ret += sum(map(len,add))
        if rm is not None:
            ret -= sum(map(len, rm))

        if update:
            self.total = ret
        return ret




if __name__ == '__main__':
    
    stdf = StdFunc()
    data = range(200)
    stdf(np.array(data))
    print stdf.delta(rm=np.array(data[100:])), np.std(data[:100])
