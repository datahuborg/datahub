import psycopg2
from datetime import datetime, date

from scorpionsql.db import *

class Query(object):
  def __init__(self, db, select, fr, where,
      group=None, order=None, limit=None):
    self.db = db
    self.select = Select(select)
    self.fr = fr
    self.where = where
    self.group = group
    self.order = order
    self.limit = limit

  tables = property(lambda self: self.fr)

  def clone(self):
    select = Select(self.select)
    fr = list(self.fr)
    where = list(self.where)
    group = self.group and list(self.group) or None
    order = self.order and list(self.order) or None
    limit = self.limit and list(self.limit) or None
    return Query(self.db, select, fr, where, group, order, limit)


  def __str__(self):
    select = str(self.select)
    fr = ','.join(self.fr)
    where = self.wherestr
    
    sql = 'SELECT %s FROM %s' % (select, fr)
    if where:
        sql = '%s WHERE %s' % (sql, where)
    if self.group:
        sql = '%s GROUP BY %s' % (sql, ','.join(list(self.group)))
    if self.order:
        sql = '%s ORDER BY %s' % (sql, ','.join(list(self.order)))
    elif self.group:
        sql = '%s ORDER BY %s' % (sql, ','.join(list(self.group)))
    if self.limit is not None:
        sql = '%s LIMIT %s' % (sql, self.limit)
    return sql

  def __wherestr__(self, where=None):
    if where is None:
      where = self.where
    where = filter(bool, list(where))
    if not where: return None
    where = ["(%s)" % clause for clause in where]
    return " and ".join(where)
  wherestr = property(__wherestr__)


  def to_outer_join_sql(self, orig_where = []):
    """
    Construct a SQL query that includes all groups that would have
    existed (exists in the orig_where clause) if the WHERE clause were not present
    """
    if not self.group:
      return str(self)

    select = str(self.select)
    fr = ','.join(self.fr)
    filter_q = "SELECT * FROM %s" % fr
    if self.where:
      filter_q += " WHERE %s" % self.wherestr

    select_clause = self.select.coalesced_str()
    groupby = ','.join(list(self.group))
    if self.order:
      orderby = ','.join(list(self.order))
    else:
      orderby = groupby

    if orig_where:
      orig_where = self.__wherestr__(orig_where)
      orig_where = ' WHERE %s' % orig_where
    else:
      orig_where = ''

    sql = """with bar as (%s)
    select %s
    from 
      ((select distinct %s from %s %s) as foo
        left outer join  
      bar using (%s)) 
    GROUP BY %s
    ORDER BY %s;""" % (filter_q, select_clause, groupby, fr, orig_where, groupby, groupby, orderby)
    print sql
    return sql

    """
    with right as (select * from lqm where WHERECLAUSE)
    select coalesce(sum(total_cost), 0), ccm_payor 
    from 
      ((select distinct ccm_payor from lqm) as payors 
        left outer join  
      right using (ccm_payor)) 
    GROUP BY ccm_payor;
    """

  def prettify(self):
    select = str(self.select)
    fr = ','.join(self.fr)
    where = self.wherestr
    
    sql = 'SELECT %s\nFROM %s' % (select, fr)
    if where:
        sql = '%s\nWHERE %s' % (sql, where)
    if self.group:
        sql = '%s\nGROUP BY %s' % (sql, ','.join(list(self.group)))
    if self.order:
        sql = '%s\nORDER BY %s' % (sql, ','.join(list(self.order)))
    if self.limit is not None:
        sql = '%s\nLIMIT %s' % (sql, self.limit)
    return sql
    


  def get_filter_qobj(self, keys=None):
    """
    Return a copy of this Query object with additional where clauses for the 
    keys in the argument
    """
    # only care about columns in aggregates right?
    cols = set()
    for agg in self.select.aggregates:
        cols.update(agg.cols)
    sels = [SelectExpr(col, [col], col, None) for col in cols]
    select = Select(sels)
    where = list(self.where)
    if keys:
      keys = list(keys)
      keys = map(sqlize, list(keys))
      expr = self.select.nonaggs[0].expr

      clause = []
      if None in keys:
        clause.append("%s is null" % expr)
      if len([k for k in keys if k is not None]) > 0:
        clause.append("%s in %%s" % expr)
      clause = " or ".join(clause)
      where.append(clause)
    else:
      where.append( '%s = %%s' % (self.select.nonaggs[0].expr ) )
    q = Query(self.db, select, self.fr, where)
    return q
    

class Select(list):
  def __init__(self, *args):
    try:
      super(Select, self).__init__(*args)
    except Exception as e:
      print e
      print args
      super(Select, self).__init__(*[args])

  def __str__(self):
    return ', '.join(map(str, self))

  def coalesced_str(self):
    return ', '.join([s.coalesced_str() for s in self])
      
  aggregates = property( lambda self: filter(lambda e: isinstance(e, SelectAgg), self) )
  aggs = property( lambda self: filter(lambda e: isinstance(e, SelectAgg), self) )    
  nonaggs = property( lambda self: filter(lambda e: not isinstance(e, SelectAgg), self) )


class SelectAgg(object):
  def __init__(self, alias, func, cols, expr, attr):
    self.alias = str(alias) if alias else None # alias, if any
    self._func = func # aggregate function
    self.cols = map(str, cols) # list of attributes 
    self.expr = expr # string of expression passed into aggregate function
    self.attr = attr # actual attribute token from sqlparse
    self.fname = attr[0]
    self.isagg = True

    #if not self.alias:
    #self.alias = str(self.fname)

  shortname = property(lambda self: self.alias or self.fname or self.expr)
  func = property(lambda self: self._func.clone())

  def __str__(self):
    s = self.expr
    if self.alias:
      s = '%s as %s' % (s, self.alias)
    return s

  def coalesced_str(self):
    s = "coalesce(%s, 0)" % self.expr
    if self.alias:
      s = "%s as %s" % (s, self.alias)
    else:
      s = "%s as %s" % (s, self.fname)
    return s

    
class SelectExpr(object):
  def __init__(self, alias, cols, expr, attr):
    self.alias = str(alias) if alias else None
    self.cols = map(str, cols)
    self.expr = expr
    self.attr = attr
    self.isagg = False

  shortname = property(lambda self: self.alias or self.expr)

  def __str__(self):
    if self.alias:
        return '%s as %s' % (self.expr, self.alias)
    return self.expr

  def coalesced_str(self):
    return str(self)


def quote_sql_str(s):
  return psycopg2.extensions.QuotedString(s).getquoted()

def sqlize(val):
  if val is None:
    return val
  if isinstance(val, basestring):
    return quote_sql_str(val)
  if isinstance(val, datetime):
    return quote_sql_str(str(val))
    if val.hour == 0 and val.minute == 0 and val.second == 0:
      return '%s::date' % quote_sql_str(str(val))
    return '%s::timestamp' % quote_sql_str(str(val))
  if isinstance(val, date):
    return quote_sql_str(str(val))
    return '%s::date' % quote_sql_str(str(val))
  return str(val)




if __name__ == '__main__':

    '(((avg(temp))) / (std(temp) + 2))'

    import pyparsing
    from pyparsing import *

        

    exprStack = []

    def pushNum(s, loc, toks):
        print 'num ', toks
    def pushVar(s, loc, toks):
        print 'var ', toks
    def pushNest(s, loc, toks):
        print 'nest ', toks
    def pushFunc(s, loc, toks):
        print 'func ', toks
    def pushArith(s, loc, toks):
        print 'arith ', toks

    def pushFirst( strg, loc, toks ):
        exprStack.append( toks[0] )
    def pushUMinus( strg, loc, toks ):
        if toks and toks[0]=='-': 
            exprStack.append( 'unary -' )
            #~ exprStack.append( '-1' )
            #~ exprStack.append( '*' )


    Number = Group(Optional("-") + Word(nums) + Optional( "." + Optional(Word(nums)))).setParseAction(pushNum)
    Var = Word(alphas).setParseAction(pushVar)
    expr = Forward()
    #foo = Forward()
    nest = Group("(" + expr + ")").setParseAction(pushNest)
    func = Group(Word(alphas) + "(" + expr + ")").setParseAction(pushFunc)
    op = Word("+_/*", max=1)

    stuff = ( func | nest | Number | Var )
    expr << (  (stuff + op + expr).setParseAction(pushArith) | stuff | Empty() )
    #foo << ( (Word("+-/*", max=1) + expr + foo) | Empty()  )
    
    res = expr.parseString("1 + 2 / foo(bar+2)")

    import pdb
    pdb.set_trace()
