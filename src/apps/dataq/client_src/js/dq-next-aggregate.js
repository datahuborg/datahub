/**
 * Helper function to return the next aggregate for a given column type.
 * ex. max, min, avg, sum, count.
 *
 * This is useful to cycle through the possible aggregates as user clicks a column.
 * col1 --click--> max(col1) --click--> min(col1), etc.
 */
(function() {
  window.DataQ = window.DataQ || {};

  // Numeric types supported in PostgreSQL.
  var number_types = ["bigint", "int8", "bigserial", "serial8", "double precision", "float8", 
    "integer", "int", "int4", "real", "float4", "smallint", "int2", "serial", "serial4"];

  // Turn number_types into a Javascript object for more efficient lookup.
  // key = PostgreSQL type, val = true iff key is a numeric type.
  var is_number = {};
  for (var i = 0; i < number_types; i++) {
    is_number[number_types[i]] = true;
  }

  // Helper for cycling through numeric aggregates.
  // key = aggregate, value = next aggregate
  // For example, a cycle (beginning at none) would be:
  // none -> max -> min -> sum -> count -> avg -> none
  var next_numeric_aggregate = {
    "none": "max",
    "max": "min",
    "min": "sum",
    "sum": "count",
    "count": "avg",
    "avg": "none"
  };

  // Helper for cycling through non-numeric aggregates.
  var next_nonnumeric_aggregate = {
    "none": "count",
    "count": "none"
  };


  /**
   * Determine the next aggregate in the cycle for the given column type and the current aggregate.
   *
   * @param columntype - The PostgreSQL type of the column.
   * @param current_aggregate - The current aggregate operator applied to the column (ex. max, min)
   *                            If no aggregate has been applied, this value should be either null
   *                            or "none".
   * @return  The next aggregate in the cycle.
   */
  DataQ.next_aggregate = function(columntype, current_aggregate) {
    if (current_aggregate === null) {
      current_aggregate = "none";
    }
    if (is_number[columntype]) {
      return next_numeric_aggregate[current_aggregate];
    } else {
      return next_nonnumeric_aggregate[current_aggregate];
    }
  };
})();
