(function($) {
  $.fn.EnhancedDataTable = function(table) {
    this.DataTable({
      "scrollX": true,
      "serverSide": true,
      "ajax": "/apps/datatables/" + table + "/"
    });
    return this;
  };
})(jQuery);
