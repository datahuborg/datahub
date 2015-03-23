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
  var tr  = $($.parseHTML("<tr></tr>")[0]);
  colDefs.forEach(function(colDef, index) {
    var name = colDef.name;
    var th =  $($.parseHTML(footer_html)[0]);
    if (index == 0) {
      th =  $($.parseHTML(first_footer_html)[0]);
    }
    tr.append(th);
    th.find("input").attr("placeholder", name);
  });
  selector.append(tr);
  return;
  $(".dataTables_scrollFootInner tfoot").each(function(index) {
    /*
    var title = jqueryObject.find('thead th').eq( $(this).index() ).text();
    $(this).attr("data-colname", title);
    $(this).append(footer_html);
    $(this).find("input").attr("placeholder", title);
    */
  });
}

var colDefs;
var jqueryContainer;
module.exports = function(container, cd) {
  jqueryContainer = container;
  colDefs = cd;
  jqueryContainer.after(or_filter_html);
};
