import json
class DrawResponse:
    def __init__(self, draw):
        self.draw = draw
        self.records_total = 0
        self.records_filtered = 0
        self.data = []
        self.error = None
    def to_json(self):
        response = {}
        response["draw"] = self.draw
        response["recordsTotal"] = self.records_total
        response["recordsFiltered"] = self.records_filtered
        response["data"] = self.data
        if self.error is not None:
            response.error["error"] = self.error
        return json.dumps(response)
    def __repr__(self):
        return "DrawResponse(draw=%s, records_total=%s, records_filtered=%s, error=%s, data=%s)" % (self.draw, self.records_total, self.records_filtered, self.error, self.data)
