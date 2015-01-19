/***
 * The modal window for editing the groupings.
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
   * @param cb - The callback to execute when the grouping has been modified. It will be executed
   *              as cb().
   */
  DataQ.GroupingModal = function(q, cb) {
    // Set the instance variables.
    query = q;
    callback = cb;

    // Create the modal HTML if it doesn't exist.
    var modal = $("#dq-grouping-modal");
    if (modal.length === 0) {
      var html = DataQ.templates["dq-grouping-modal"]({
        columns: query.grouping()
      });
      $("body").append(html);
    }

    // Display the modal.
    $("#dq-grouping-modal").modal({
      backdrop: "static",
      keyboard: false
    });

    // When the modal is displayed, enable iCheck and HTML5Sortable.
    $("#dq-grouping-modal").on("shown.bs.modal", function() {
      $(".dq-grouping-modal-list").sortable({
        forcePlaceholderSize: true 
      });
    });
  }; // End GroupingModal

  // Handler for close modal.
  $(document).on("click", "#dq-grouping-modal-quit-btn", function() {
    callback();
    $("#dq-grouping-modal").remove();
  });

  // Handle for finishing edits.
  $(document).on("click", "#dq-grouping-modal-done-btn", function() {
    var new_grouping = [];

    // Iterate through each list item (in order).
    $(".dq-grouping-list-item").each(function() {
      var li = $(this);
      var string = li.data("string");
      var grouping = query.grouping();
      var current_group;

      // Find the group associated with this list item.
      query.grouping().forEach(function(group) {
        if (group.string === string) {
          current_group = group;
        }
      });

      new_grouping.push(current_group);
    });

    query.grouping(new_grouping);
    callback();
    $("#dq-grouping-modal").remove();
  });

})();
