var grouped_buttons_template = require("./templates/grouped-aggregate-dropdown.hbs");
var api = require("./api.js");
var col_list_items_template = require("./templates/aggregate-col-list-item.hbs");
var PostgresTypes = require("./postgres-types.js");

var colDefs;
var jqueryContainer;
var postgres_types;
var repo;
var table;
var current_aggregate;
module.exports = function(container, cd, r, tbl) {
  var that = {};
  postgres_types = PostgresTypes();
  colDefs = cd;
  repo = r;
  table = tbl;
  jqueryContainer = container;

  jqueryContainer.append(grouped_buttons_template());
  return that;
}

$(document).on('click', '.dt-agg-item', function() {
  // Hide the result.
  $(".dt-agg-result").css("visibility", "hidden");

  // Make the column list div visible.
  var col_agg_div = $('.dt-col-agg-div');
  col_agg_div.css("visibility", "visible");

  // Clear all items in the column list.
  var list = $('.dt-col-agg-list');
  list.html("");

  // Figure out the aggregation operator being applied.
  var agg_type = $(this).data("agg-type");
  current_aggregate = agg_type;
  var agg_type_text = $(this).html();

  // Display the type in the dropdown button text.
  $('.dt-agg-type').html(agg_type_text + " ");

  // Figure out which columns this aggregator can be applied to.
  var supported_cols = colDefs
  .filter(function(item) {
    return postgres_types.can_apply(agg_type, item.type);
  });

  if (supported_cols.length > 0) {
    // Clear the button content of the aggregate column name.
    $(".dt-col-agg-name").html("Column Name...");
  } else {
    $(".dt-col-agg-name").html("No Supported Columns...");
  }

  // Create the list items.
  var list_html = col_list_items_template({"colDefs": supported_cols});
  list.html(list_html);
});

$(document).on("click", ".dt-col-agg-item", function() {
  $(".dt-agg-result").css("visibility", "hidden");
  var agg_type = current_aggregate;
  var col_name = $(this).html();
  $(".dt-col-agg-name").html(col_name + " ");
  api.compute_aggregate(repo, table, agg_type, col_name, function(err, data) {
    var result = err;
    if (err === null) {
      result = data;
    }
    $(".dt-agg-result")
      .css("visibility", "visible")
      .html(" = " + result);
  });
});
