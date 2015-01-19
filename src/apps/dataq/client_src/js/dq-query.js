/**
 * The object for building a query.
 */
(function() {
  // If the DataQ object doesn't exist, create it.
  window.DataQ = window.DataQ || {};

  DataQ.Query = function() {
    
    // Create the object and initialize the objects.
    var that = {};
    that._schema_for_table_name = {};
    that._repo_name = null;
    that._operated_column = null;
    that._selected_columns_for_table = {};
    that._filter_for_code = {};
    that._grouping = [];
    that._sorts = {};

    /**
     * Get or set the schema for a given table.
     *
     * @param table_name - The name of the table.
     * @param schema - If this argument is omitted (or undefined), this function acts as a getter
     *                returning the schema for the given table. Otherwise, the function acts as a 
     *                setter, setting the schema for table_name.
     *
     * @return The schema for the table name.
     */
    that.schema = function(table_name, schema) {
      if (schema !== undefined) {
        that._schema_for_table_name[table_name] = schema;
      } 
      return that._schema_for_table_name[table_name];
    };

    /**
     * Get or set the repo name.
     *
     * @param repo_name - If this argument is omitted (or undefined), this function acts as a 
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The name of the repo.
     */
    that.repo = function(repo_name) {
      if (repo_name !== undefined) {
        that._repo_name = repo_name;
      }
      return that._repo_name;
    };

    /**
     * Get or set the operated column.
     *
     * @param operated_column - if this argument is omitted (or undefined), this function acts as
     *                          a getter. Otherwise, it acts a setter, setting the operated column.
     *
     * @return The name of the operated column ("table.col"). This may be null.
     */
    that.operated_column = function(operated_column) {
      if (operated_column !== undefined) {
        that._operated_column = operated_column;
      }
      return that._operated_column;
    };

    that.update_grouping = function() {
      that._grouping = [];
      var has_operated_column = false;
      for (var table in that._selected_columns_for_table) {
        if (!that._selected_columns_for_table[table]) {
          continue;
        }
        that._selected_columns_for_table[table].forEach(function(column) {
          if (column.agg === "none") {
            that._grouping.push({
              "string": table + "." + column.name,
              "table": table,
              "column": column
            });
          } else {
            has_operated_column = true;
          }
        });
      } // end for each table

      if (!has_operated_column) {
        that._grouping = [];
      }
    };

    that.selected_columns = function(table_name, selected_columns) {
      if (selected_columns !== undefined) {
        that._selected_columns_for_table[table_name] = selected_columns;
      }
      return that._selected_columns_for_table[table_name];
    };

    that.get_selected_tables = function() {
      var tbls = [];
      for (var k in that._selected_columns_for_table) {
        tbls.push(k);
      }
      return tbls;
    };

    that.add_filter = function(filter1, op, filter2) {
      var filter_string = filter1 + " " + op + " " + filter2;
      var code = md5((new Date()).getTime() + filter_string);
      that._filter_for_code[code] = {
        "filter1": filter1,
        "op": op,
        "filter2": filter2,
        "filter_string": filter_string
      };
      return that._filter_for_code[code];
    };

    that.delete_filter = function(code) {
      that._filter_for_code[code] = undefined;
    };

    that.get_filters = function() {
      var result = [];
      for (var k in that._filter_for_code) {
        var filter = that._filter_for_code[k];
        if (!filter) {
          continue;
        }
        result.push({
          "code": k,
          "filter1": filter.filter1,
          "op": filter.op,
          "filter2": filter.filter2,
          "filter_string": filter.filter_string
        });
      };
      return result;
    };

    that.grouping = function(grouping) {
      if (grouping !== undefined) {
        that._grouping = grouping;
      }
      return that._grouping;
    };

    that.add_sort = function(sort) {
      that._sorts[sort.string] = sort;
    };

    that.delete_sort = function(sort) {
      that._sorts[sort] = undefined;
    };

    that.sorts = function() {
      var result = [];
      for (var k in that._sorts) {
        if (that._sorts[k] !== undefined) {
          result.push(that._sorts[k]);
        }
      }
      return result;
    };

    return that;
  };
})();
