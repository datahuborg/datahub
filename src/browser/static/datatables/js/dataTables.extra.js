(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
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
      "dom": 'RC<"clear">lfrtip',
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

},{"./api.js":2,"./filter-footer.js":3}],2:[function(require,module,exports){
/**
 * This file contains the code for interacting with the API
 * for server side processing of datatables.
 */

// The root of the API.
var url_base = "/apps/datatables/api/";


// The object that will contain the API functions.
var api = {};


/**
 * Given a repo name and table name, construct the URL
 * which DataTables.js should request in order to get a
 * table draw.
 */
api.table_url = function(repo, table) {
  return url_base + "table/" + repo + "/" + table + "/";
}

/**
 * Given a repo name and table name, determine the schema of the table
 * and return a columnDefs (https://datatables.net/reference/option/columnDefs)
 * which is usable by DataTables.
 *
 * The callback is triggered as callback(err, columnDefs), where columnDefs is a
 * columnDef configuration for DataTables. If there is no error, err will be null.
 * Otherwise, it is a string indicating the error.
 */
api.get_column_definitions = function(repo, table, callback) {
  // Create the endpoint URL.
  var url = url_base + "schema/" + repo + "/" + table + "/";

  // Get the schema.
  $.get(url, function(schema_result) {

    // Parse if there's a success.
    if (schema_result.success) {
      var schema = schema_result.schema;
      var columnDefinitions = [];

      // Create the columnDefs.
      schema.forEach(function(column, index) {
        columnDefinitions.push({
          "name": column[0],
          "targets": index
        });
      });

      // Trigger the callback.
      callback(null, columnDefinitions);
    } else {
      callback("Failed columnDefs request");
    }
  });
}

module.exports = api;

},{}],3:[function(require,module,exports){
var footer_html = require("./html/filter_footer.html");
var first_footer_html = require("./html/first_filter_footer.html");
var or_filter_html = require("./html/filter_buttons.html");

var nextOp = {
  "=": "!=",
  "!=": "<",
  "<": "<=",
  "<=": ">",
  ">": ">=",
  ">=": "btw a;b",
  "btw a;b": "="
};

$(document).on("click", ".dt-op-button", function() {
  $(this).text(nextOp[$(this).text()]);
  datatable.draw();
});

$(document).on("click", ".dt-invert-filter", function() {
  datatable.draw();
});

$(document).on("click", ".dt-new-filter", function() {
  createFilter();
});

$(document).on("click", ".dt-delete-button", function() {
  // Delete the entire row.
  // button < span < div < th < tr
  $(this).parent().parent().parent().parent().remove();
});

$(document).on("keyup change", ".dt-filter input[type=text]", function() {
  datatable.draw();
});

var createFilter = function(){
  var selector = $(".dataTables_scrollFootInner tfoot"); 
  var tr  = $($.parseHTML("<tr class='dt-filter'></tr>")[0]);
  var order = datatable.colReorder.order();

  for (var i = 0; i < order.length; i++) {
    colDefs.forEach(function(colDef, index) {
      if (colDef.targets !== order[i]) {
        return;
      }
      var name = colDef.name;
      var th =  $($.parseHTML(footer_html)[0]);
      if (index == 0) {
        th =  $($.parseHTML(first_footer_html)[0]);
      }
      tr.append(th);
      th.find("input").attr("placeholder", name);
      th.attr("data-colname", colDef.name);
    });
    selector.append(tr);
  }
}

var colDefs;
var jqueryContainer;
var datatable;
module.exports = function(container, cd, dt) {
  var that = {};

  jqueryContainer = container;
  colDefs = cd;
  datatable = dt;
  jqueryContainer.after(or_filter_html);

  that.filters = function() {
    var filters = [];
    $(".dt-filter").each(function() {
      var filter = [];
      $(this).find("th").each(function() {
        var colname = $(this).data("colname");
        var filter_text = $(this).find("input[type=text]").val();
        var filter_op = $(this).find(".dt-op-button").text();
        
        // Sometimes DataTables.js will create duplicate copies of the filters. If so,
        // then we cannot extract the desired values, so we skip this "false filter".
        if (filter_text === undefined) {
          return;
        }

        if (filter_text.length > 0) {
          filter.push({
            "colname": colname,
            "filter_text": filter_text,
            "filter_op": filter_op
          });
        }
      });
      if (filter.length > 0) {
        filters.push(filter);
      }
    });
    return filters;
  };

  that.isInverted = function() {
    return $(".dt-invert-filter").prop("checked");
  };

  return that;
};

},{"./html/filter_buttons.html":4,"./html/filter_footer.html":5,"./html/first_filter_footer.html":6}],4:[function(require,module,exports){
module.exports = "<button class=\"btn btn-primary dt-new-filter\">New Filter</button>\n<label class=\"btn btn-primary\">\n  <input class=\"dt-invert-filter\" type=\"checkbox\" autocomplete=\"off\"> Invert Filter\n</label>\n";

},{}],5:[function(require,module,exports){
module.exports = "<th>\n  <div class=\"input-group\">\n    <span class=\"input-group-btn\">\n      <button class=\"btn btn-default dt-op-button\" type=\"button\">=</button>\n    </span>\n    <input type=\"text\" class=\"form-control dt-filtertext\" placeholder=\"Filter...\">\n  </div>\n</th>\n";

},{}],6:[function(require,module,exports){
module.exports = "<th>\n  <div class=\"input-group\">\n    <span class=\"input-group-btn\">\n      <button class=\"btn btn-danger dt-delete-button\" type=\"button\"><i class=\"fa fa-trash\"></i></button>\n      <button class=\"btn btn-default dt-op-button\" type=\"button\">=</button>\n    </span>\n    <input type=\"text\" class=\"form-control\" placeholder=\"Filter...\">\n  </div>\n</th>\n";

},{}]},{},[1]);
