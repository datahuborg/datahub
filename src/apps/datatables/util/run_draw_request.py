from core.db.manager import DataHubManager 
class RunDrawRequest:
    def __init__(self, repo, table, draw_request, draw_response, manager):
        self.repo = repo
        self.table = table
        self.draw_request = draw_request
        self.draw_response = draw_response
        self.manager = manager
    def run(self):
        print self.draw_response
        data = self.manager.execute_sql("select * from insurance.insurance LIMIT 10;")
        data = data['tuples']
        self.draw_response.records_total = len(data)
        self.draw_response.records_filtered = len(data) 
        self.draw_response.data = data
        return self.draw_response
