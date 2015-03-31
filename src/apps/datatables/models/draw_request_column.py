'''
Represents a column in the draw request from DataTables.js.
'''
class DrawRequestColumn:
    def __init__(self, data, name, searchable, orderable, searchValue, searchRegex):
        self.data = data
        self.name = name
        self.searchable = searchable
        self.orderable = orderable
        self.searchValue = searchValue
        self.searchRegex = searchRegex
    def __repr__(self):
        return "Col(data=%s, name=%s, searchable=%s, orderable=%s, searchRegex=%s)" % (self.data, self.name, self.searchable, self.orderable, self.searchRegex)
    __str__ = __repr__
