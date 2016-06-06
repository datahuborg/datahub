from functools import wraps
import json

from core.db.manager import DataHubManager

from util import pick

dbwipes_repo = 'dbwipes_cache'
dbwipes_table = 'dbwipes_cache'


def does_cache_exist(repo_base):
    """ check to see if the cache exists for the repo base"""
    manager = DataHubManager(repo_base)
    repo_exists = False
    table_exists = False
    schema_correct = False

    # check for repo
    if dbwipes_repo in manager.list_repos():
        repo_exists = True

    # check for table
    if repo_exists and dbwipes_table in manager.list_tables(dbwipes_repo):
        table_exists = True

    # check for schema
    schema = None
    if table_exists:
        schema = manager.get_schema(dbwipes_repo, dbwipes_table)

    if schema == [('key', 'character varying'), ('val', 'text')]:
        schema_correct = True

    return repo_exists and table_exists and schema_correct


def create_cache(username):
    """ DBWipes stores some metadata about the table in a schema in the owner's
        database. Note that this is not necessarily the current user's DB
    """
    try:
        query = ('create table if not exists %s.dbwipes_cache'
                 '(key varchar, val text)') % dbwipes_repo
        manager = DataHubManager(user=username)
        manager.create_repo(dbwipes_repo)
        manager.execute_sql(query)
        return True
    except Exception as e:
        print(e)
        return False


def insert_into_cache(f):
    """Inserts metadata into the cache"""
    @wraps(f)
    def _f(self, *args, **kwargs):
        try:
            key = str(map(str, (f.__name__, self.repo, self.tablename,
                                self.where, self.nbuckets, map(str, args))))
            query = 'select val from {}.dbwipes_cache where key = %s'.format(
                dbwipes_repo)

            manager = DataHubManager(user=self.repo_base)
            vals = manager.execute_sql(query, (key,))['tuples']

            if len(vals) > 0:
                return json.loads(vals[0][0])
        except Exception as e:
            print(e)

        res = f(self, *args, **kwargs)
        if key:
            value = json.dumps(res, default=json_handler)
            params = (key, value)
            q = 'insert into ' + dbwipes_repo + '.dbwipes_cache values(%s, %s)'

            manager = DataHubManager(user=self.repo_base)
            manager.execute_sql(q, params)

        return res
    return _f


def json_handler(o):
    if hasattr(o, 'isoformat'):
        return o.isoformat()


class Summary(object):

    def __init__(self, repo, tablename, username, repo_base=None,
                 nbuckets=50, where=''):
        self.username = username
        self.repo_base = repo_base
        self.repo = repo
        self.tablename = tablename
        self.nbuckets = nbuckets
        self.where = ''
        where = where.strip()
        if where:
            self.where = 'WHERE %s' % where

        # make sure cache exists
        # create_cache(username)

        self.nrows = self.get_num_rows()
        self.col_types = self.get_columns_and_types()

    def __call__(self):
        stats = []
        for col, typ in self.col_types:
            # print "stats for: %s\t%s" % (col, typ)
            col_stats = self.get_col_stats(col, typ)
            if col_stats is None:
                # print "\tgot None"
                continue
            # print "\tgot %d" % (len(col_stats))
            stats.append((col, typ, col_stats))
        return stats

    def close(self):
        pass

    def reset_cache(self):
        q = "delete from cache where key like '%%%%%s%%%%%s%%%%'" % (
            str(self.engine), self.tablename)
        manager = DataHubManager(user=self.username, repo_base=self.username)
        manager.execute_sql(q)

    def query(self, q, *args):
        """
        Summaries using other engines only need to override this method
        """
        manager = DataHubManager(user=self.username, repo_base=self.repo_base)
        return manager.execute_sql(q, params=args)['tuples']

    @insert_into_cache
    def get_num_rows(self):
        q = "SELECT count(*) from %s" % self.tablename
        return self.query(q)[0][0]

    @insert_into_cache
    def get_distinct_count(self, col):
        q = "SELECT count(distinct %s) FROM %s %s" % (
            col, self.tablename, self.where)
        return self.query(q)[0][0]

    @insert_into_cache
    def get_column_counts(self, cols):
        q = 'SELECT %s FROM %s'
        select = ["count(distinct %s)" % col for col in cols]
        select = ", ".join(select)
        q = q % (select, self.tablename)
        counts = tuple(self.query(q)[0])
        return dict(zip(cols, counts))

    @insert_into_cache
    def get_columns_and_types(self):
        manager = DataHubManager(user=self.username, repo_base=self.repo_base)

        tokens = self.tablename.split('.')
        repo = tokens[0]
        table = tokens[1]

        rows = manager.get_schema(repo, table)
        ret = []
        for col, typ in rows:
            if typ == 'text':
                typ = 'str'
            if 'double' in typ:
                typ = 'num'
            if 'int' in typ:
                typ = 'num'
            if 'date' in typ or 'time' in typ:
                typ = 'time'
            ret.append((str(col), str(typ)))
        return ret

    @insert_into_cache
    def get_columns(self):
        """
        engine specific way to get table columns
        """
        return pick(self.get_columns_and_types(), 0)

    @insert_into_cache
    def get_type(self, col_name):
        return dict(self.get_columns_and_types()).get(col_name, None)

    def get_col_groupby(self, col_name, col_type):
        if col_type is None:
            return None

        groupby = None

        if 'time' == col_type:
            groupby = self.get_time_stats(col_name)

        if 'date' in col_type or 'timestamp' in col_type:
            groupby = self.get_date_stats(col_name)

        return groupby

    @insert_into_cache
    def get_col_stats(self, col_name, col_type=None):
        if col_type is None:
            col_type = self.get_type(col_name)

        # if col_type.startswith('_'):
        # return None

        numerics = ['int', 'float', 'double', 'numeric', 'num']
        chars = ['char', 'text', 'str']

        is_numeric = col_type in numerics
        is_char = col_type in chars

        if is_numeric:
            return self.get_numeric_stats(col_name)
        elif is_char:
            return self.get_char_stats(col_name)

        groupby = self.get_col_groupby(col_name, col_type)
        if groupby:
            stats = self.get_group_stats(col_name, groupby)
            return stats
        return None

    def get_group_stats(self, col_name, groupby):
        q = ('select %s as GRP, min(%s), max(%s), count(*) '
             'from %s  %s group by GRP '
             'order by GRP limit %d')
        q = q % (groupby, col_name, col_name,
                 self.tablename, self.where, self.nbuckets)
        rows = [{'val': x, 'count': count, 'range': [minv, maxv]}
                for (x, minv, maxv, count) in self.query(q)]
        return rows

    def get_numeric_stats(self, c):
        ndistinct = self.get_distinct_count(c)
        if ndistinct == 0:
            return []
        if ndistinct == 1:
            if self.where:
                q = "SELECT %s from %s %s AND %s is not null"
                args = (c, self.tablename, self.where, c)
            else:
                q = "SELECT %s from %s WHERE %s is not null"
                args = (c, self.tablename, c)
            val = self.query(q % args)[0][0]
            return [{'val': val, 'count': self.nrows, 'range': [val, val]}]

        q = """
          with TMP as (
            SELECT 2.5 * stddev(%s) / %d as block FROM %s %s
          )
          SELECT (%s/block)::int*block as bucket,
                 min(%s) as min,
                 max(%s) as max,
                 count(*) as count
          FROM %s,  TMP
          %s
          GROUP BY bucket
          ORDER BY bucket
          """
        q = q % (c, self.nbuckets, self.tablename, self.where,
                 c, c, c, self.tablename, self.where)

        stats = []
        for (val, minv, maxv, count) in self.query(q):
            if val is None:
                stats.append({
                    'val': None,
                    'count': count,
                    'range': [minv, maxv]
                })
            else:
                stats.append({
                    'val': (maxv + minv) / 2.,
                    'count': count,
                    'range': [minv, maxv]
                })

        return stats

    def get_char_stats(self, col_name):
        q = """
            select %s as GRP, min(%s), max(%s), count(*)
            FROM %s
            %s
            GROUP BY GRP
            ORDER BY count(*) desc
            LIMIT %d
            """
        q = q % (col_name, col_name, col_name,
                 self.tablename, self.where, self.nbuckets)
        rows = [{'val': x, 'count': count, 'range': [minv, maxv]}
                for (x, minv, maxv, count) in self.query(q)]
        return rows

    def get_time_stats(self, col_name):
        return "date_trunc('hour', %s)::time" % col_name

    def get_date_stats(self, col_name):
        q = ('select max(%s)::date, min(%s)::date, '
             'EXTRACT(EPOCH FROM (max(%s::timestamp) - min(%s::timestamp)))/60'
             ' as minutes from %s')
        q = q % (col_name, col_name, col_name, col_name, self.tablename)
        (maxv, minv, nminutes) = self.query(q)[0]
        if maxv is None or minv is None or nminutes is None:
            return None

        ndays = nminutes / 60 / 24

        var = "%s::timestamp" % col_name

        if ndays == 0:
            groupby = "date_trunc('hour', %s)" % var
        elif ndays <= 30:
            groupby = "date_trunc('day', %s)" % var
        elif ndays <= 50 * 7:
            groupby = "date_trunc('week', %s)" % var
        elif ndays <= 365 * 12:
            groupby = "date_trunc('month', %s)" % var
        else:
            groupby = "date_trunc('year', %s)" % var
        return groupby
