(function($) {
  var url_base = "/apps/datatables/api/";
  $.fn.EnhancedDataTable = function(repo, table) {
    var url_table = url_base + "table/" + repo + "/" + table + "/";
    var url_schema = url_base + "schema/" + repo + "/" + table + "/";
    var thisDataTable = this;

    // First get the schema so we can set the column names.
    $.get(url_schema, function(schema_result) {
      if (schema_result.success) { // Was the schema retrieved successfully?

        // Create the column definitions to put into the data table.
        var columnDefinitions = [];
        var schema = schema_result.schema;
        for (var i = 0; i < schema.length; i++) {
          columnDefinitions.push({
            "name": schema[i][0],
            "targets": i
          });
        }

        /*
        // Add buttons to add an "And" or "Or".
        var addButton = $("<button class='btn btn-primary'>+And</button>");
        // Add a section to the bottom of each column for computing aggregates.
        thisDataTable.find('tfoot th').each( function () {
            var title = thisDataTable.find('thead th').eq( $(this).index() ).text();
            $(this).html( '<input type="text" placeholder="Filter '+title+'" />\n<button>Here</button>' );
        } );
        */
             
        thisDataTable.DataTable({
          "columnDefs": columnDefinitions,
          "searching": false,
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
