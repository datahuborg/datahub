/**
 * Logic for constructing a SQL query string from a DataQ.Query object.
 */
(function() {
  // If the global DataQ object does not exist, create it.
  window.DataQ = window.DataQ || {};

  /**
   * Take a DataQ.Query object and generate a SQL query string from it.
   *
   * @param query - The DataQ.Query object.
   * @return A String representing the SQL query.
   */
  window.DataQ.build_query = function(query) {

    // The list of columns to select.
    var select_list = [];

    // The list of tables to select from.
    var from_list = [];

    // The filters to apply.
    var where_list = [];

    // The grouping to perform.
    var group_list = [];

    // The sorting to apply.
    var order_list = [];

    // Get the current repo name - we'll need to prepend this to some of the table/column names.
    var repo = query.repo();

    // Create the FROM clause. It is simply the list of tables that the user has selected.
    // Each item in the list is a String of the form: "repo.table".
    query.get_selected_tables().forEach(function(table) {
      from_list.push(repo + "." + table);
    });

    // Create the SELECT clause.
    // Iterate through every selected column of every selected table and add the column to the 
    // select list (and write the aggregate if possible).
    query.get_selected_tables().forEach(function(table) {
      query.selected_columns(table).forEach(function(column) {
        if (column.agg === undefined || column.agg === null || column.agg === "none") {
          select_list.push(repo + "." + table + "." + column.name);
        } else {
          // When an aggregate "agg" on column "col" in table "table" and repo "repo" appears, mark
          // "agg(repo.table.col) as agg_table_col".
          select_list.push(column.agg + "(" + repo + "." + table + "." + column.name + ")" + 
            " as " + column.agg + "_" + table + "_"
            + column.name);
        }
      });
    });

    // Create the WHERE clause.
    // Simply iterate through each filter and add it to the list.
    query.get_filters().forEach(function(filter) {
      where_list.push(filter.filter1 + " " + filter.op + " " + filter.filter2);
    });

    // Create the  GROUP BY clause.
    query.grouping().forEach(function(group) {
      var agg = group.column.agg;

      // We can only add a group by if it's not the aggregate column.
      if (agg === null || agg === undefined || agg === "none") {
        group_list.push(repo + "." + group.string);
      } 
    });

    // Create the ORDER BY clause.
    query.sorts().forEach(function(sort) {
      var agg = sort.column.agg;
      if (agg === null || agg === undefined || agg === "none") {
        order_list.push(repo + "." + sort.string);
      } else {
        order_list.push(agg + "_" + sort.table + "_" + sort.column.name);
      }
    });

    // Set the query string.
    if (select_list.length === 0) {
      return "";
    }
    var query_string = "SELECT " + select_list.join(", ")
        + " FROM " + from_list.join(", ");

    // Set the where list.
    if (where_list.length > 0) {
      query_string +=  " WHERE " + where_list.join(" AND ");
    }

    // Set the group list.
    if (group_list.length > 0) {
      query_string += " GROUP BY " + group_list.join(", ")
    }

    // Set the order list.
    if (order_list.length > 0) {
      query_string += " ORDER BY " + order_list.join(", ")
    }

    // Remove leading and trailing spaces and then append semicolon.
    query_string.trim();
    query_string += ";";
    return query_string;
  };
})();
