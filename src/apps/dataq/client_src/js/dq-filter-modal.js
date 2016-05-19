/**
 * The modal window that allows the user to create filters (of the form <val1> <operation> <val2>).
 *
 * The modal window is a bootstrap modal.
 */
(function() {
  // If the global DataQ object does not exist, create it.
  window.DataQ = window.DataQ || {};

  // The callback to trigger when the modal is closed. This is executed as callback().
  var callback;
  
  // The DataQ.Query object being built.
  var query;

  /**
   * Launch the modal.
   *
   * @param q - The DataQ.Query object being built.
   * @param cb - The callback to execute when the filter has been added. It will be executed
   *                   as cb().
   */
  DataQ.FilterModal = function(q, cb) {
    // Set the instance variables.
    callback = cb;
    query = q;

    // If the modal does not exist, create it.
    var modal = $("#dq-filter-modal");
    if (modal.length === 0) {
      var columns = [];

      // Iterate through each column of each selected table and add to the list of columns.
      query.get_selected_tables().forEach(function(selected_table) {
        query.schema(selected_table).forEach(function(column) {
          columns.push({
            "column_name": column[0],
            "table_name": selected_table,
            "full_name": selected_table + "." + column[0]
          });
        });
      });

      // Create the HTML for the filter modal.
      var html = DataQ.templates['dq-filter-modal']({
        "columns": columns,
        "repo": query.repo() 
      });

      // Add the modal to the page.
      $('body').append(html);
    }

    // Display the modal (disable Esc)
    $('#dq-filter-modal').modal({
      keyboard: false
    });

    // Handle modal close when clicking backdrop.
    $(".modal-backdrop").click(function() {
      callback();
      $("#dq-filter-modal").remove();
    })
  } // End FilterModal

  // Handle modal close.
  $(document).on("click", ".dq-filter-quit", function() {
    callback();
    $("#dq-filter-modal").remove();
  });

  // Handle modal done.
  $(document).on("click", ".dq-filter-done", function() {
    var filter1 = $('.dq-filter-1-text').val();
    var filter2 = $('.dq-filter-2-text').val();
    var op = $('.dq-filter-op-text').val();
    if (filter1.length > 0 && filter2.length > 0 && op.length > 0) {
      query.add_filter(filter1, op, filter2);
      callback();
      $('#dq-filter-modal').modal('hide');
      $("#dq-filter-modal").remove();
    } else {
      alert("You need to fill out the three text boxes");
    }
  });

  // Handle filter1 dropdown link click (in <filter1> <operation> <filter2>)
  $(document).on("click", ".dq-filter-1-link", function() {
    $('.dq-filter-1-text').val($(this).html());
  });

  // Handle filter2 dropdown link click (in <filter1> <operation> <filter2>)
  $(document).on("click", ".dq-filter-2-link", function() {
    $('.dq-filter-2-text').val($(this).html());
  });

  // Handle operation dropdown link click (in <filter1> <operation> <filter2>)
  $(document).on("click", ".dq-filter-op-link", function() {
    // Unescape html for > and <
    var op = $(this).html().replace("&gt;", ">").replace("&lt;", "<");
    $('.dq-filter-op-text').val(op);
  });

})();
