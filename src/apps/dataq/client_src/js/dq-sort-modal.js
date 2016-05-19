/**
 * The modal window that allows the user to specify the sorting of the columns.
 *
 * The modal window is a bootstrap modal.
 */
(function() {
  // If the global DataQ object does not exist, create it.
  window.DataQ = window.DataQ || {};

  // The callback to trigger whent he modal is closed.
  var callback;

  // The DataQ.Query object being built.
  var query;

  /**
   * Launch the modal.
   *
   * @param q - The DataQ.Query object being built.
   * @param cb - The callback to trigger when the user finishes specifying sorts. It is executed as
   *              cb().
   */
  DataQ.SortModal = function(q, cb) {
    // Set the instance variables.
    query = q;
    callback = cb;

    // If the modal HTML does not exist, add it to the page.
    var modal = $("#dq-sort-modal");
    if (modal.length === 0) {
      var html = DataQ.templates['dq-sort-modal']();
      $('body').append(html);
    }

    // Display the modal (disable Esc)
    $('#dq-sort-modal').modal({
      keyboard: false
    });

    // When the modal is shown, populate the columns.
    $("#dq-sort-modal").on("shown.bs.modal", function() {
      update_list();
    });

    // Handle modal close when clicking backdrop.
    $(".modal-backdrop").click(function() {
      $("#dq-sort-modal").remove();
      callback();
    })
  };

  // Handle dropdown item click.
  $(document).on("click", ".dq-sort-modal-dropdown-btn", function() {
    var list = $('.dq-sort-modal-dropdown');
    list.html("");

    // When a dropdown link is clicked, add it to the list of selected columns.
    create_items_in_dropdown().forEach(function(item) {
      list.append(DataQ.templates["dq-sort-dropdown-li"]({
        "item": item
      }));
    });

  });

  // Create the items in the sort dropdown menu.
  var create_items_in_dropdown = function() {
    // Identify the sorts that have already been used.
    var used_dict = {};
    query.sorts().forEach(function(sort) {
      used_dict[sort.string] = true;
    });

    // Iterate through every column of every selected table and, if it isn't used, add it to the 
    // list of items.
    var items = [];
    query.get_selected_tables().forEach(function(selected_table) {
      query.selected_columns(selected_table).forEach(function(column) {
        var string = selected_table + "." + column.name;
        if (column.agg !== "none") {
          string = column.agg + "(" + selected_table + "." + column.name + ")";
        }

        // Don't add any item to dropdown if it's already used.
        if (used_dict[string]) {
          return;
        }

        items.push({
          "string": string,
          "table": selected_table,
          "column": column
        });

      });
    });

    return items;
  };

  // Add the list items to list of used sorts.
  var update_list = function() {
    var list = $('.dq-sort-item-list');
    list.html("");
    query.sorts().forEach(function(sort) {
      var html = DataQ.templates["dq-sort-list-item"]({
        "item": sort 
      });
      list.append(html);
    });
  };

  // Handle modal close.
  $(document).on("click", ".dq-sort-modal-quit", function() {
    $('#dq-sort-modal').remove();
    callback();
  });

  // Handle sort clicked.
  $(document).on("click", ".dq-sort-link", function() {
    var li = $(this);
    var name = li.data("columnname");
    var type = li.data("columntype");
    var agg = li.data("aggregate");
    var table = li.data("table");
    var string = li.data("string");

    if (agg === undefined || agg === null) {
      agg = "none";
    }

    var item = {
      "column": {
        "name": name,
        "type": type,
        "agg": agg
      },
      "string": string,
      "table": table
    };

    query.add_sort(item);
    update_list();

  });

  // Handle modal close.
  $(document).on("click", ".dq-sort-modal-done-btn", function() {
    $('#dq-sort-modal').remove();
    callback();
  });

  // Handle delete sort.
  $(document).on("click", ".dq-sort-delete-btn", function() {
    var li = $(this).parent().parent();
    var string = li.data("string");
    query.delete_sort(string);
    update_list();
  });

})();
