'''
Represents an order in the draw request from DataTables.js.
'''
class DrawRequestOrder:
    def __init__(self, column, direction):
        self.column = column
        self.direction = direction
    def __repr__(self):
        return "Ord(column=%s, direction=%s)" % (self.column, self.direction)
    __str__ = __repr__
