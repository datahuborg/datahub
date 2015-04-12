var filter_buttons_template = require("./templates/filter_buttons.hbs");
var filter_template = require("./templates/filter.hbs");
var delete_button_col = require("./templates/delete-button-col.hbs");

var hidden_cols = {};

var set_visibility = function(colname, visibility) {
  if (visibility !== undefined) {
    if (visibility) {
      hidden_cols[colname] = undefined;
    } else {
      hidden_cols[colname] = true;
    }
  }
  var hidden = hidden_cols[colname] === true;
  var th_selector = $(".dt-filter th[data-colname=" + colname + "]");
  if (hidden) {
    th_selector.hide();
  } else {
    th_selector.show();
  }
}; 

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
  var order = datatable.colReorder.order();

  for (var i = 0; i < order.length; i++) {
    for (var j = 0; j < colDefs.length; j++) {
      if (colDefs[j].targets === order[i]) {
        colDefs[j].order = i;
      }
    }
  }

  colDefs.sort(function(a, b) {
    if (a.order < b.order) {
      return -1;
    } else if (a.order > b.order) {
      return 1;
    } else {
      return 0;
    }
  });

  selector.append(filter_template({"colDefs": colDefs}));

  for (var colname in hidden_cols) {
    set_visibility(colname);
  }

}

var colDefs;
var jqueryContainer;
var datatable;
var colvis;
module.exports = function(container, cd, dt) {
  var that = {};

  jqueryContainer = container;
  colDefs = cd;
  datatable = dt;

  jqueryContainer.append(filter_buttons_template());

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

  that.set_visibility = function(colNum, visibility) {
    for (var i = 0; i < colDefs.length; i++) {
      if (colDefs[i].targets === colNum) {
        set_visibility(colDefs[i].name, visibility);
      }
    }
  }

  that.get_hidden_col_dict = function() {
    return hidden_cols;
  }

  that.onReorder = function() {
    $('.dt-delete-button').remove();
    $('.dt-filter th:first-child').each(function() {
      var old_val = $(this).find("input").val();
      $(this).html(delete_button_col({
        "name": $(this).data("colname"),
        "value": old_val
      }));;
    });
  };
  return that;
};
