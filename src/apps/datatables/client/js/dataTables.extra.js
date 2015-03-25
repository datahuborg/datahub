var api = require("./api.js");
var FilterBar = require("./filter-bar.js");

$.fn.EnhancedDataTable = function(repo, table, callback) {
  // The jquer object for which the EnhancedDataTable function was triggered.
  var jqueryObject = this;
  var filterBar;

  // Get the column definitions for this table.
  api.get_column_definitions(repo, table, function(err, columnDefs) {
    if (err !== null) {
      console.log("Failed to get column defs");
      return;
    }

    // Create the DataTable.
    var datatable = jqueryObject.DataTable({
      "dom": 'RC<"clear">lfrtip',
      "columnDefs": columnDefs,
      "searching": false,
      "scrollX": true,
      "serverSide": true,
      "ajax": {
        "url": api.table_url(repo, table),
        "data": function(d) {
          if (filterBar !== undefined) {
            d["filters"] = filterBar.filters();
            d["filterInverted"] = filterBar.isInverted();
          }
        }
      },
      "colVis": {
        "overlayFade": 0,
        "stateChange": function(colNum, visibility) {
          filterBar.set_visibility(colNum, visibility);
        }
      },
      "initComplete": function(settings, json) {
        filterBar = FilterBar(jqueryObject.parent().parent(), columnDefs, datatable);
      },
      "drawCallback": function(settings) {
        var json_result = datatable.ajax.json();
        var query = json_result.query;
        callback(query);
      }
    });
  });

  return this;
};
