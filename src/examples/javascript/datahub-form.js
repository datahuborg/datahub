$(document).ready(function () {
    var transport = new Thrift.Transport("http://datahub.csail.mit.edu/service/json"),
    protocol = new Thrift.Protocol(transport),
    client = new DataHubClient(protocol),
    con_params = new ConnectionParams({'user': 'anantb', 'password': 'anant'}),
    con = client.open_connection(con_params),

    prepareSubmit = function() {
        var self = $(this),
        table = self.attr("datahub-table"),
        insertVals = function(names, values) {
            query = "INSERT INTO " + 
                    table + "(" + names.join(", ") + ") " +
                    "VALUES ('" + values.join("', '") + "')"
            client.execute_sql(con, query)
        },
        submit = function(e) {
            var i,
            inputs = self.serializeArray()
            e.preventDefault();
            names = []
            values = []
            for (i=0; i<inputs.length; i++) {
                names.push(inputs[i].name)
                values.push(inputs[i].value)
            }
            insertVals(names, values)
            return false;
        }
        self.submit(submit);
    };

    $('form.datahub').each(prepareSubmit);
});