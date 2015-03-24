var api = require("./api.js");
var FilterFooter = require("./filter-footer.js");

$.fn.EnhancedDataTable = function(repo, table) {
  // The jquer object for which the EnhancedDataTable function was triggered.
  var jqueryObject = this;
  var filterFooter;

  // Get the column definitions for this table.
  api.get_column_definitions(repo, table, function(err, columnDefs) {
    if (err !== null) {
      console.log("Failed to get column defs");
      return;
    }

    // Create the DataTable.
    var datatable = jqueryObject.DataTable({
      "columnDefs": columnDefs,
      "searching": false,
      "scrollX": true,
      "serverSide": true,
      "ajax": {
        "url": api.table_url(repo, table),
        "data": function(d) {
          if (filterFooter !== undefined) {
            d["filters"] = filterFooter.filters();
            d["filterInverted"] = filterFooter.isInverted();
          }
        }
      },
      "initComplete": function(settings, json) {
        filterFooter = FilterFooter(jqueryObject.parent().parent(), columnDefs, datatable);
      },
      "drawCallback": function(settings) {
        //console.log(datatable.ajax.json());
      }
    });
  });

  return this;
};
