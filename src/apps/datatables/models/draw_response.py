import json
import decimal

class DrawResponse:
    def __init__(self, draw):
        self.draw = draw
        self.records_total = 0
        self.records_filtered = 0
        self.data = []
        self.query = ""
        self.error = None
    def to_json(self):
        response = {}
        response["draw"] = self.draw
        response["recordsTotal"] = self.records_total
        response["recordsFiltered"] = self.records_filtered
        response["data"] = self.data
        response["query"] = self.query
        if self.error is not None:
            response.error["error"] = self.error
        return json.dumps(response, default=strange_data_handler)

    def __repr__(self):
        return "DrawResponse(draw=%s, records_total=%s, records_filtered=%s, error=%s, data=%s, query=%s)" % (self.draw, self.records_total, self.records_filtered, self.error, self.data, self.query)


def strange_data_handler(obj):
    ''' used to handle datetime objects, 
        which json_dumps will otherwise choke on. '''
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    else:
        obj