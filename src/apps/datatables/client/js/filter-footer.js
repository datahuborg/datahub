var footer_html = require("./html/filter_footer.html");
var first_footer_html = require("./html/first_filter_footer.html");
var or_filter_html = require("./html/filter_buttons.html");

var nextOp = {
  "=": "!=",
  "!=": "<",
  "<": "<=",
  "<=": ">",
  ">": ">=",
  ">=": "="
};

$(document).on("click", ".dt-op-button", function() {
  $(this).text(nextOp[$(this).text()]);
});


$(document).on("click", ".dt-new-filter", function() {
  createFilter();
});

$(document).on("click", ".dt-delete-button", function() {
  // Delete the entire row.
  // button < span < div < th < tr
  $(this).parent().parent().parent().parent().remove();
});

var createFilter = function(){
  var selector = $(".dataTables_scrollFootInner tfoot"); 
  var tr  = $($.parseHTML("<tr class='dt-filter'></tr>")[0]);
  colDefs.forEach(function(colDef, index) {
    var name = colDef.name;
    var th =  $($.parseHTML(footer_html)[0]);
    if (index == 0) {
      th =  $($.parseHTML(first_footer_html)[0]);
    }
    tr.append(th);
    th.attr("data-colname", colDef.name);
    th.find("input").attr("placeholder", name);
  });
  selector.append(tr);
}

var colDefs;
var jqueryContainer;
module.exports = function(container, cd) {
  var that = {};

  jqueryContainer = container;
  colDefs = cd;
  jqueryContainer.after(or_filter_html);

  that.filters = function() {
    var filters = [];
    $(".dt-filter").each(function() {
      var filter = [];
      $(this).find("th").each(function() {
        var colname = $(this).data("colname");
        var filter_text = $(this).find("input[type=text]").val();
        var filter_op = $(this).find(".dt-op-button").text();
        if (filter_text.length > 0) {
          filter.push({
            "colname": colname,
            "filter_text": filter_text,
            "filter_op": filter_op
          });
        }
      });
      if (filter.length > 0) {
        filters.push(filter);
      }
    });
    return filters;
  };

  return that;
};
