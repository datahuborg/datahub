from django.http import HttpRequest
from draw_request_column import DrawRequestColumn
from draw_request_order import DrawRequestOrder

'''
Class for parsing draw request from DataTables.js and converting into a SQL query.
Refer to http://www.datatables.net/manual/server-side for more information about how this request
is constructed.
'''
class DrawRequest:
    '''
    Create the instance using a django.http.HttpRequest object.
    The request must have all the parameters specified in http://www.datatables.net/manual/server-side
    in the GET parameters. Otherwise, the initializer will throw an exception.
    '''
    def __init__(self, request):
        # First extract the easy variables.
        self.draw = request.GET["draw"]
        self.start = request.GET["start"]
        self.length = request.GET["length"]
        self.searchValue = request.GET["search[value]"]
        self.searchRegex = request.GET["search[regex]"]


        # Next, we'll extract the columns and order.
        # We don't know how many of them there are, so we'll have to
        # loop through until we hit the end.
        self.columns = []
        self.order = []
        moreCols = True 
        moreOrds = True 
        i = 0
        while moreOrds or moreCols:
            # Extract the order, if there is one.
            order_column_fmt = "order[%d][column]" % (i,)
            order_dir_fmt = "order[%d][dir]" % (i,)
            if order_column_fmt in request.GET:
                order_column = request.GET[order_column_fmt]
                order_dir = request.GET[order_dir_fmt]
                self.order.append(DrawRequestOrder(order_column, order_dir))
            else:
                moreOrds = False

            # Extract the column, if there is one.
            column_data_fmt = "columns[%d][data]" % (i,)
            column_name_fmt = "columns[%d][name]" % (i,)
            column_searchable_fmt = "columns[%d][searchable]" % (i,)
            column_orderable_fmt = "columns[%d][orderable]" % (i,)
            column_search_value_fmt = "columns[%d][search][value]" % (i,)
            column_search_regex_fmt = "columns[%d][search][regex]" % (i,)
            if column_data_fmt in request.GET:
                column_data = request.GET[column_data_fmt]
                column_name = request.GET[column_name_fmt]
                column_searchable = request.GET[column_searchable_fmt]
                column_orderable = request.GET[column_orderable_fmt]
                column_search_value = request.GET[column_search_value_fmt]
                column_search_regex = request.GET[column_search_regex_fmt]
                self.columns.append(DrawRequestColumn(column_data, column_name, column_searchable, column_orderable, column_search_value, column_search_regex))
            else:
                moreCols = False

            # Move on to the next element.
            i += 1
    def __repr__(self):
        return "DrawRequest(draw=%s, start=%s, length=%s, searchValue=%s, searchRegex=%s, columns=%s, order=%s)" % (self.draw, self.start, self.length, self.searchValue, self.searchRegex, self.columns, self.order) 
    __str__ = __repr__
