var footer_html = require("./html/filter_footer.html");
var first_footer_html = require("./html/first_filter_footer.html");
var or_filter_html = require("./html/filter_buttons.html");

var nextOp = {
  "=": "!=",
  "!=": "<",
  "<": "<=",
  "<=": ">",
  ">": ">=",
  ">=": "btw a;b",
  "btw a;b": "="
};

$(document).on("click", ".dt-op-button", function() {
  $(this).text(nextOp[$(this).text()]);
  datatable.draw();
});

$(document).on("click", ".dt-invert-filter", function() {
  datatable.draw();
});

$(document).on("click", ".dt-new-filter", function() {
  createFilter();
});

$(document).on("click", ".dt-delete-button", function() {
  // Delete the entire row.
  // button < span < div < th < tr
  $(this).parent().parent().parent().parent().remove();
});

$(document).on("keyup change", ".dt-filter input[type=text]", function() {
  datatable.draw();
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
    th.find("input").attr("placeholder", name);
    th.attr("data-colname", colDef.name);
  });
  selector.append(tr);
}

var colDefs;
var jqueryContainer;
var datatable;
module.exports = function(container, cd, dt) {
  var that = {};

  jqueryContainer = container;
  colDefs = cd;
  datatable = dt;
  jqueryContainer.after(or_filter_html);

  that.filters = function() {
    var filters = [];
    $(".dt-filter").each(function() {
      var filter = [];
      $(this).find("th").each(function() {
        var colname = $(this).data("colname");
        var filter_text = $(this).find("input[type=text]").val();
        var filter_op = $(this).find(".dt-op-button").text();
        
        // Sometimes DataTables.js will create duplicate copies of the filters. If so,
        // then we cannot extract the desired values, so we skip this "false filter".
        if (filter_text === undefined) {
          return;
        }

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

  that.isInverted = function() {
    return $(".dt-invert-filter").prop("checked");
  };

  return that;
};
