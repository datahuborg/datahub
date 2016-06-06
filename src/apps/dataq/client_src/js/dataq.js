/**
 * Defines the DataQ.DQ object, which is what the user of the library will interact with.
 *
 * Simply call DataQ.DQ(repo_name, callback) and DataQ will launch. After the user builds a query,
 * the callback is executed as callback(query), where query is a String representing the SQL query 
 * or null if the query was not built successfully.
 */
(function() {
  // Create the global DataQ object if it doesn't exist.
  window.DataQ = window.DataQ || {};

  // The DataQ.Query that is being built.
  query = null;

  // The callback to execute after the query is built. It is executed as cb(query) where query
  // is a String representing the SQL query or null if the query was not built.
  var callback;

  /**
   * @param repo_name - The name of the repo that DataQ should work on.
   * @param cb - The callback to trigger when the query is built.
   */
  DataQ.DQ = function(repo_name, cb) {
    // Set the callback.
    callback = cb;

    // Add the container to the page.
    var container = $(DataQ.templates["dataq-container"]());
    $('body').append(container);

    // Create the query object and set the repo name.
    query = DataQ.Query();
    query.repo(repo_name);

    // Handle DataQ close when clicking backdrop.
    $(".dq-black-background").click(function() {
      $(".dq-black-background").remove();
      $(".dataq").remove();
      callback(null);
    })
  };

  /**
   * Update the UI to reflect the latest query.
   */
  var display_query = function() {

    /**********************************/
    /*** 1: Selected Tables/Columns ***/
    /**********************************/
    $('.dq-selected-tables').html("");
    query.get_selected_tables().forEach(function(selected_table) {
      var selected_columns = query.selected_columns(selected_table);
      if (selected_columns === null) {
        return;
      }

      // Go through each column for the table and add it to the column list.
      var column_list = [];
      selected_columns.forEach(function(selected_column) {
        if (selected_column.agg === "none") {
          column_list.push(selected_column.name);
        } else {
          // If col has an aggregate, write it as "aggregate(col)".
          column_list.push(selected_column.agg + "(" + selected_column.name + ")");
        }
      });

      // Add the table and column list to the UI.
      var html = DataQ.templates["dq-selected-table"]({
        "table_name": selected_table,
        "column_list": column_list.join(", ")
      });
      $('.dq-selected-tables').append(html);
    });

    /***************************/
    /*** 2: Selected Filters ***/
    /***************************/
    $('.dq-filter-list').html("");
    query.get_filters().forEach(function(filter) {
      $('.dq-filter-list').append(DataQ.templates['dq-filter-list-item']({
        "filter": filter
      }));
    });

    /**************************/
    /*** 3: Selected Groups ***/
    /**************************/
    // Identify which groups are checked.
    var group_strings = [];
    query.grouping().forEach(function(group) {
      group_strings.push(group.string);
    });

    // Display the groups.
    if (group_strings.length > 0) {
      $(".dq-grouping-text").html(group_strings.join(", "));
    } else {
      $(".dq-grouping-text").html("No Grouping...");
    }

    /************************************/
    /*** 4: Identify the Sort Columns ***/
    /************************************/
    var sort_strings = [];
    query.sorts().forEach(function(sort) {
      sort_strings.push(sort.string);
    });
    
    // Display the sorts.
    if (sort_strings.length > 0) {
      $(".dq-sorting-text").html(sort_strings.join(", "));
    } else {
      $(".dq-sorting-text").html("No Sorting...");
    }

  }; // end display_query

  // Handle table additions.
  $(document).on("click", ".dq-btn-add-table", function() {
    DataQ.TableModal(query, null, display_query);
  });

  // Handle table deletes.
  $(document).on("click", ".dq-btn-delete-table", function() {
    var table_name = $(this).data("tablename");
    if (query.operated_column() && query.operated_column().split(".")[0] === table_name) {
      query.operated_column(null);
    }
    query.selected_columns(table_name, null);
    query.update_grouping();
    display_query();
  });

  // Handle table edits.
  $(document).on("click", ".dq-btn-edit-table", function() {
    DataQ.TableModal(query, $(this).data("tablename"), display_query);
  });

  // Handle filter additions.
  $(document).on("click", ".dq-btn-add-filter", function() {
    DataQ.FilterModal(query, display_query);
  });

  // Handle filter deletion.
  $(document).on("click", ".dq-btn-delete-filter", function() {
    var code = $(this).parent().data("code");
    query.delete_filter(code);
    display_query();
  });

  // Handle grouping edit.
  $(document).on("click", ".dq-btn-edit-grouping", function() {
    DataQ.GroupingModal(query, display_query);
  });

  // Handle sorting edit.
  $(document).on("click", ".dq-btn-edit-sorting", function() {
    DataQ.SortModal(query, display_query);
  });

  // Handle DataQ cancel.
  $(document).on("click", ".dq-btn-cancel-query", function() {
    $(".dq-black-background").remove();
    $(".dataq").remove();
    callback(null);
  });

  // Handle DataQ run query.
  $(document).on("click", ".dq-btn-run-query", function() {
    $(".dq-black-background").remove();
    $(".dataq").remove();
    callback(DataQ.build_query(query));
  });
})();
