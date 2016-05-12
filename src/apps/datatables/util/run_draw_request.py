from core.db.manager import DataHubManager 


class RunDrawRequest:
    def __init__(self, repo, table, draw_request, draw_response, manager):
        self.repo = repo
        self.table = table
        self.draw_request = draw_request
        self.draw_response = draw_response
        self.manager = manager

    def run(self):
        select_clause = self.select_clause()
        from_clause = self.from_clause()
        where_clause = self.where_clause()
        order_by_clause = self.order_by_clause()
        limit_offset_clause = self.limit_offset_clause()
        sql = "%s %s %s %s %s;" % (select_clause, from_clause, where_clause, order_by_clause, limit_offset_clause) 
        self.draw_response.query = "%s %s %s %s;" % (select_clause, from_clause, where_clause, order_by_clause)
        data = self.manager.execute_sql(sql)
        data = data['tuples']
        self.draw_response.records_total = self.num_tuples(False)
        if len(self.where_clause()) == 0:
            self.draw_response.records_filtered = self.draw_response.records_total
        else:
            self.draw_response.records_filtered = self.num_tuples(True)
        self.draw_response.data = data
        return self.draw_response

    def select_clause(self):
        return "SELECT " + ", ".join([col.name for col in self.draw_request.columns])

    def where_clause(self):
        # Figure out the types of the columns so we'll know whether to use
        # numeric operations or string operations.
        schema = self.manager.get_schema(self.repo, self.table)
        type_for_col = {}
        for column in schema:
            type_for_col[column[0]] = column[1]

        if len(self.draw_request.filters) > 0: 
            inverted = self.draw_request.filterInverted
            list_filters = []
            for table_filter in self.draw_request.filters: # Iterate through each filter.
                list_filter = []
                for col_filter in table_filter: # Iterate through each column filter.
                    op = col_filter.operation
                    text = col_filter.text
                    if "btw" in op:
                        range_vals = text.split(";")
                        if len(range_vals) != 2:
                            return ""
                        first, second = range_vals[0], range_vals[1]
                        if type_for_col[col_filter.name] == "text":
                            first = "'" + first + "'"
                            second = "'" + second + "'"
                        col_filter_string = "(%s BETWEEN %s AND %s)" % (col_filter.name, first, second)
                    if type_for_col[col_filter.name] == "text": # Change the op and text for string comparison.
                        if op == "=":
                            text = "'%" + text + "%'"
                            op = "ILIKE"
                        elif op == "!=":
                            text = "'%" + text + "%'"
                            op = "NOT ILIKE"
                        elif "btw" not in op:
                            text = "'" + text + "'"
                    if "btw" not in op:
                        col_filter_string = "(%s %s %s)" % (col_filter.name, op, text)
                    list_filter.append(col_filter_string)
                table_filter_string = " AND ".join(list_filter)
                table_filter_string = "(%s)" % (table_filter_string,)
                list_filters.append(table_filter_string)

            clause = " OR ".join(list_filters)
            if inverted:
                clause = "NOT (%s)" % (clause,)
            return "where " + clause
        return ""

    def num_tuples(self, with_where_clause):
        where_clause = ""
        if with_where_clause:
            where_clause = self.where_clause()
        data = self.manager.execute_sql("SELECT COUNT(*) %s %s" % (self.from_clause(), where_clause))
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
