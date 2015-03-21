from core.db.manager import DataHubManager 
class RunDrawRequest:
    def __init__(self, repo, table, draw_request, draw_response, manager):
        self.repo = repo
        self.table = table
        self.draw_request = draw_request
        self.draw_response = draw_response
        self.manager = manager
    def run(self):
        sql = "select * %s %s %s %s;" % (self.from_clause(), self.where_clause(), self.order_by_clause(), self.limit_offset_clause())
        data = self.manager.execute_sql(sql)
        data = data['tuples']
        print sql
        self.draw_response.records_total = self.num_tuples()
        self.draw_response.records_filtered = self.num_tuples()
        self.draw_response.data = data
        return self.draw_response
    def where_clause(self):
        clause = ""
        if len(self.draw_request.searchValue) > 0:
            searchVal = self.draw_request.searchValue
            colStrings = []
            for column in self.draw_request.columns:
                colStrings.append("%s ILIKE '%%%s%%'" % (column.name, searchVal))
            if len(colStrings) > 0:
                return "WHERE %s" % (" OR ").join(colStrings)
        return ""
    def num_tuples(self):
        data = self.manager.execute_sql("SELECT COUNT(*) FROM %s.%s" % (self.repo, self.table))
        return int(data['tuples'][0][0])
    def from_clause(self):
        return "from %s.%s" % (self.repo, self.table)
    def limit_offset_clause(self):
        return "LIMIT %s OFFSET %s" % (self.draw_request.length, self.draw_request.start)
    def order_by_clause(self):
        sql = "ORDER BY "
        order_strings = []
        for order in self.draw_request.order:
            column = self.draw_request.columns[order.column].name
            order_strings.append("%s %s" % (column, order.direction))
        if len(order_strings) > 0:
            sql = sql + ", ".join(order_strings)
        else:
            return "ORDER BY %s" % (self.draw_request.columns[0].name,)
        return sql
