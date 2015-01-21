/**
 * The modal window that allows the user to select the tables (and columns from these tables) that
 * they want to use in their query.
 *
 * This modal can be used to either ADD a new table (and some of its columns) to the query or to
 * EDIT an existing table (and its columns) that is already in the query.
 *
 * The modal window is a bootstrap modal.
 */
(function() {
  // If the global DataQ object does not exist, create it.
  window.DataQ = window.DataQ || {};

  // The callback to trigger when the modal is closed.
  var cb;

  // The table we have selected.
  var table;

  // The DataQ.Query object being built.
  var query;

  /**
   * Launch the modal.
   *
   * @param q - The DataQ.Query object being built.
   *
   * @param table_name - The name of the table to modify. This must be either null (in which case
   * the "Add Table" modal is displayed), or a table which the current user is associated with.
   *
   * @param callback - The callback that is executed after the user finishes updating selections.
   * It is executed as callback()
   */
  DataQ.TableModal = function(q, table_name, callback) {
    table = table_name;
    cb = callback;
    query = q;

    // If the modal HTML does not exist, add it to the page.
    var modal = $("#dq-table-modal");
    if (modal.length === 0) {
      var html = DataQ.templates['dq-table-modal']({
        "table_name": table 
      });
      $('body').append(html);
    }

    // Display the modal (disable Esc and clicking the backdrop to exit modal)
    $('#dq-table-modal').modal({
      backdrop: 'static',
      keyboard: false
    });
    
    // Don't allow clicking Done until the user selects a table.
    $(".dq-modal-done-btn").hide();

    // When the modal is shown, populate the columns.
    $("#dq-table-modal").on("shown.bs.modal", function() {
      if (table) {
        populate_column_list(table);
      }
    });
  }; 

  // If the user quits, trigger the callback.
  $(document).on('click', '.dq-modal-quit', function() {
    $("#dq-table-modal").remove();
    cb();
  });


  // If the user clicks the table dropdown, populate the list with the list
  // of available tables.
  $(document).on("click", ".dq-modal-dropdown-btn", function() {
    var dropdown = $(".dq-modal-dropdown");
    dropdown.html("");
    DataQ.API.get_tables(query.repo(), function(data) {
      data.tables.forEach(function(table) {
        var html = DataQ.templates["dq-modal-dropdown-item"]({
          "item_name": table
        });
        dropdown.append(html);
      }); // end foreach
    }) // get_tables
  }); // document on click


  // When a table is selected from the dropdown, create the column list.
  $(document).on("click", ".dq-modal-dropdown-link", function() {
    // Set the content of the dropdown.
    var item_name = $(this).data("item_name");
    table = item_name;
    $('.dq-modal-table-dropdown-text').text(table);
    populate_column_list();
  });

  // Populate the list of columns with the schema of the given table.
  var populate_column_list = function() {
    // Get the schema for the selected tables.
    DataQ.API.get_schema(query.repo(), table, function(data) {
      $(".dq-modal-done-btn").show();

      // Sort the columns by name.
      query.schema(table, data.schema).sort(function(a, b) {return a[0] > b[0]});

      // Create the HTML and add it to the UI.
      var html = DataQ.templates["dq-modal-columns"]({
        "columns": query.schema(table)
      });
      $('.dq-column-list').html(html);

      // Enable iCheck.
      $('.dq-column-list input[type=checkbox]').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
      });

      if (query.selected_columns(table)) {
        // Iterate through the columns for the selected table.
        query.selected_columns(table).forEach(function(column) {
          // Extract the data entries from the element (we find the element by selecting
          // .dq-modal-column[data-columnname="colname"]
          var element = $('.dq-modal-column[data-columnname="'+column.name+'"]');
          element.data("columnname", column.name);
          element.data("columntype", column.type);
          element.data("currentaggregate", column.agg || "none")
          element.find("input[type=checkbox]").iCheck('check');
          if (column.agg !== "none") {
            element.find("button").text(column.agg + "(" + column.name + ")");
          }
        }); // end forEach
      } // if selected columns
    });
  };

  // Handle column aggregate trigger.
  $(document).on("click", ".dq-modal-column button", function() {
    // Extract the data entries.
    var parent_li = $(this).parent();
    var columnname = parent_li.data("columnname");
    var columntype = parent_li.data("columntype");
    var currentaggregate = parent_li.data("currentaggregate")

    // Compute the next aggregate operator to apply.
    var nextaggregate = DataQ.next_aggregate(columntype, currentaggregate);

    // If an aggregate has already been applied, don't apply another.
    if (query.operated_column() !== table + "." + columnname && query.operated_column() !== null) {
      nextaggregate = "none";
    }

    // If the aggregate has been turned off, turn off the operated column.
    // Else if this is the new operated column, indicate so.
    if (nextaggregate === "none") {
      if (query.operated_column() === table + "." + columnname) {
        query.operated_column(null);
      }
      $(this).text(columnname);
    } else {
      $(this).text(nextaggregate + "(" + columnname + ")");
      query.operated_column(table + "." + columnname);
    }
    parent_li.data("currentaggregate", nextaggregate);
  });

  // When this is clicked, return the selected columns.
  $(document).on("click", ".dq-modal-done-btn", function() {
    // Figure out the selected columns.
    var columns = [];
    var is_op_col_checked = false;

    // Iterate through each of the columns.
    $('.dq-modal-column').each(function() {
      var li = $(this);

      // If the column is checked.
      if (li.find("input").is(":checked")) {

        // Extract the data entries.
        var agg = li.data("currentaggregate");
        var type = li.data("columntype");
        var name = li.data("columnname");

        // If the operated column has been selected, then mark it so.
        if (table + "." + name === query.operated_column()) {
          is_op_col_checked = true;
        }

        if (agg === null || agg === undefined) {
          agg = "none";
        }

        columns.push({
          "name": name,
          "type": type,
          "agg": agg
        });

      }
    });

    // If the operated column should be in this table and has not been selected,
    // set the operated column as null.
    if (query.operated_column() && 
        query.operated_column().split(".")[0] === table && 
        !is_op_col_checked) {
      query.operated_column(null);
    }

    // Mark the selected columns for this table, and recompute the tables.
    query.selected_columns(table, columns);
    query.update_grouping();

    // Remove the modal from the page.
    $("#dq-table-modal").remove();
    cb();
  });

})();
