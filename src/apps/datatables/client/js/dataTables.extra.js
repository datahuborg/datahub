var api = require("./api.js");
var FilterBar = require("./filter-bar.js");
var table_header_template = require("./templates/table_header.hbs");
var shorten_query = require("./shorten-query.js");

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
    
    var table_header_html = table_header_template({"colDefs": columnDefs});
    jqueryObject.find("thead").html(table_header_html);
    jqueryObject.find("tfoot").html(table_header_html);

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
          var json_result = datatable.ajax.json();
          var query = json_result.query;
          query = shorten_query(query, filterBar.get_hidden_col_dict());
          callback(query);
        }
      },
      "initComplete": function(settings, json) {
        filterBar = FilterBar(jqueryObject.parent().parent(), columnDefs, datatable);
      },
      "drawCallback": function(settings) {
        var json_result = datatable.ajax.json();
        var query = json_result.query;
        callback(shorten_query(query))
      }
    });
  });

  return this;
};
