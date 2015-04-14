'''
Represents a single filter on a column.
'''
class DrawRequestColumnFilter:
    '''
    Initialize the filter with the column name, filter text,
    and operation (must be "=", "<=", ">=", "<", ">", or "!=").
    '''
    def __init__(self, column_name, filter_text, operation):
        self.name = column_name
        self.text = filter_text
        self.operation = operation
    def __repr__(self):
        return "ColFilter(name=%s, text=%s, op=%s)" % (self.name, self.text, self.operation)
    __str__ = __repr__
