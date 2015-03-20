(function($) {
  var url_base = "/apps/datatables/api/";
  $.fn.EnhancedDataTable = function(repo, table) {
    var url_table = url_base + "table/" + repo + "/" + table + "/";
    var url_schema = url_base + "schema/" + repo + "/" + table + "/";
    var thisDataTable = this;

    $.get(url_schema, function(schema_result) {
      if (schema_result.success) {
        var columnDefinitions = [];
        var schema = schema_result.schema;
        for (var i = 0; i < schema.length; i++) {
          columnDefinitions.push({
            "name": schema[i][0],
            "targets": i
          });
        }
        console.log(columnDefinitions);

        thisDataTable.DataTable({
          "columnDefs": columnDefinitions,
          "scrollX": true,
          "serverSide": true,
          "ajax": "/apps/datatables/api/table/" + repo + "/" + table + "/"
        });
      } else {
        alert("failed to load table");
      }
    });
    return this;
  };
})(jQuery);
