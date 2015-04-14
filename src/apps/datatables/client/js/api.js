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
          "type": column[1],
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

api.compute_aggregate = function(repo, table, agg_type, col_name, callback) {
  var url = url_base + "aggregate/" + repo + "/" + table + "/" + agg_type + "/" + col_name + "/";
  $.get(url, function(aggregate_result) {
    if (aggregate_result.success) {
      callback(null, aggregate_result.value);
    } else {
      callback("Aggregate failed");
    }
  });
};

module.exports = api;
