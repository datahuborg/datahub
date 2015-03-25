var api = require("./api.js");
var FilterBar = require("./filter-bar.js");

$.fn.EnhancedDataTable = function(repo, table, callback) {
  // The jquer object for which the EnhancedDataTable function was triggered.
  var jqueryObject = this;
  var filterBar;

  var shorten_query = function(query) {
    try {
      var lower_case_query = query.toLowerCase();
      var select_end = lower_case_query.indexOf("select") + "select".length;
      var from_start = lower_case_query.indexOf("from");
      var select_string = query.substring(select_end, from_start);
      var select_arr = select_string.trim().split(",");

      var hidden_cols = filterBar.get_hidden_col_dict();
      var new_select_arr = [];
      var colname;
      for (var i = 0; i < select_arr.length; i++) {
        colname = select_arr[i].trim();
        if (hidden_cols[colname] === true) {
          continue;
        }
        new_select_arr.push(colname);
      }

      var final_query = query.substring(0, select_end) + " " + new_select_arr.join(", ") + " " + query.substring(from_start);
      return final_query;
    } catch (ex) {
      return query;
    }
  };

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
          var json_result = datatable.ajax.json();
          var query = json_result.query;
          query = shorten_query(query);
          console.log(query);
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
