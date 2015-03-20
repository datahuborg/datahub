'''
Represents an order in the draw request from DataTables.js.
'''
class DrawRequestOrder:
    def __init__(self, column, direction):
        self.column = column
        self.direction = direction
