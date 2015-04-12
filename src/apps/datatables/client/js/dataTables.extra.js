var api = require("./api.js");
var FilterBar = require("./filter-bar.js");
var Aggregator = require("./aggregator.js");
var table_header_template = require("./templates/table_header.hbs");
var shorten_query = require("./shorten-query.js");

$.fn.EnhancedDataTable = function(repo, table, query_callback, init_callback) {
  // The jquer object for which the EnhancedDataTable function was triggered.
  var jqueryObject = this;
  var filterBar;
  var aggregator;

  // Get the column definitions for this table.
  api.get_column_definitions(repo, table, function(err, columnDefs) {
    if (err !== null) {
      console.log("Failed to get column defs");
      return;
    }
    
    var table_header_html = table_header_template({"colDefs": columnDefs});
    jqueryObject.find("thead").html(table_header_html);
    jqueryObject.find("tfoot").html(table_header_html);

    // Update the filter bar when a column visibility changes.
    jqueryObject.on( 'column-visibility.dt', function ( e, settings, column, state ) {
      filterBar.set_visibility(column, state);
      var json_result = datatable.ajax.json();
      var query = json_result.query;
      query = shorten_query(query, filterBar.get_hidden_col_dict());
      query_callback(query);
    });

    // Create the DataTable.
    var datatable = jqueryObject.DataTable({
      "dom": 'RClfrt<"inlineblock"i><"inlineblock floatright"p><"clear">',
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
      "colReorder": {
        "reorderCallback": function() {
          filterBar.onReorder();
        }
      },
      "colVis": {
        "overlayFade": 0,
        "label": function(index, title, th) {
          var MAX_LENGTH = 12;
          var colname = $(th).data("colname");
          if (colname.length > MAX_LENGTH + "...".length) {
            return colname.substr(0, MAX_LENGTH) + "..."
          } else {
            return colname;
          }
        },
        "stateChange": function() {
          // This function is unreliable! Don't override it!
        }
      },
      "initComplete": function(settings, json) {
        filterBar = FilterBar(jqueryObject.parent().parent().parent(), columnDefs, datatable);
        aggregator = Aggregator(jqueryObject.parent().parent().parent(), columnDefs, repo, table);

        datatable.forEachRowInColumn = function(colName, func) {
          var targets = -1;
          columnDefs.forEach(function(columnDef) {
            if (columnDef.name === colName) {
              targets = columnDef.targets;
            }
          });
          if (targets === -1) {
            throw "Invalid column name";
          }

          var colIndex = -1;
          datatable.colReorder.order().forEach(function(target, index) {
            if (targets === target) {
              colIndex = index;
            }
          });
          if (colIndex === -1) {
            throw "Not a valid reordering";
          }

          jqueryObject.find("tbody tr").each(function(row_index) {
            $(this).find("td").each(function(index) {
              if (index === colIndex) {
                var value = $(this).html();
                var node = $(this);
                func(value, node, row_index);
              }
            });
          });
        };

        datatable.getColDef = function() {
          return columnDefs;
        };

        if (init_callback !== undefined) {
          init_callback(datatable);
        }
      },
      "drawCallback": function(settings) {
        var json_result = datatable.ajax.json();
        var query = json_result.query;
        query_callback(shorten_query(query))
      }
    });
    $(".ColVis_Button")
      .removeClass("ColVis_Button")
      .removeClass("ColVis_MasterButton")
      .addClass("btn")
          .addClass("btn-primary");
  });

  return this;
};
