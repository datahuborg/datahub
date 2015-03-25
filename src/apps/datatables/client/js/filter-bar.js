var filter_buttons_template = require("./templates/filter_buttons.hbs");
var filter_template = require("./templates/filter.hbs");

var hidden_cols = {};

var get_order = function(colname) {
  var order = datatable.colReorder.order();
  var targets = 0;
  colDefs.forEach(function(colDef) {
    if (colDef.name === colname) {
      targets = colDef.targets;
    }
  });
  for (var i = 0; i < order.length; i++) {
    if (targets === order[i]) {
      return i + 1;
    }
  }
};

var set_visibility = function(colname) {
  var hidden= hidden_cols[colname] === true;
  var th_selector = $(".dt-filter th[data-colname=" + colname + "]");
  var colheader_selector = $(".dataTables_scrollHeadInner tr[role=row] th[data-colname=" + colname + "]");
  var colbody_selector = $(".dataTables_scrollBody tbody tr td:nth-child(" + get_order(colname) + ")");
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

$(document).on("click", ".dt-hidden-list input[type=checkbox]", function() {
  var colname = $(this).val();
  if ($(this).prop("checked")) {
    hidden_cols[colname] = true;
    set_visibility(colname);
  } else {
    hidden_cols[colname] = undefined;
    set_visibility(colname);
  }
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
  var selector = $(".dataTables_scrollHeadInner thead"); 
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

  selector.prepend(filter_template({"colDefs": colDefs}));

  for (var colname in hidden_cols) {
    set_visibility(colname);
  }

}

var colDefs;
var jqueryContainer;
var datatable;
module.exports = function(container, cd, dt) {
  var that = {};

  jqueryContainer = container;
  colDefs = cd;
  datatable = dt;

  var colnames = [];
  colDefs.forEach(function(colDef) {
    colnames.push(colDef.name);
  });
  colnames.sort();
  jqueryContainer.before(filter_buttons_template({"colnames": colnames}));

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

  that.visibilityToggled = function(colName, visibility) {
    return;
    var selector = $(".dt-filter th[data-colname=" + colName + "]");
    if (visibility) {
      selector.show();
    } else {
      selector.hide();
    }
  };

  return that;
};
