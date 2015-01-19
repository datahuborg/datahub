this["DataQ"] = this["DataQ"] || {};
this["DataQ"]["templates"] = this["DataQ"]["templates"] || {};
this["DataQ"]["templates"]["dataq-container"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<!-- HTML file containing the overall DataQ interface -->\n\n<!-- Create a translucent black background -->\n<div class=\"dq-black-background\"></div>\n\n<!-- The DataQ container -->\n<div class=\"dataq container-fluid\">\n\n  <!-- Section 1: Select columns -->\n  <div class=\"row dq-section\">\n    <div class=\"dq-circle hidden-xs col-sm-1\">1</div>\n    <h3 class=\"dq-title col-xs-11\">Select columns</h3>\n  </div>\n\n  <!-- The table section HTML goes inside this div -->\n  <div class=\"dq-table-section-container\">\n  </div>\n\n  <!-- Section 2: Filter out rows -->\n  <div class=\"row dq-section\">\n    <div class=\"dq-circle hidden-xs col-sm-1\">2</div>\n    <h3 class=\"dq-title col-xs-11\">Filter out some rows</h3>\n  </div>\n\n  <!-- The filter section HTML goes inside this div -->\n  <div class=\"dq-selected-filters\">\n      <ul class=\"dq-filter-list\"></ul>\n  </div>\n\n  <!-- Button to add a new filter -->\n  <div class=\"row\">\n    <button class=\"btn btn-primary dq-btn-add-filter col-xs-offset-1\">Add Filter</button>\n  </div>\n\n  <!-- Section 3: Groupings -->\n  <div class=\"row dq-section\">\n    <div class=\"dq-circle hidden-xs col-sm-1\">3</div>\n    <h3 class=\"dq-title col-xs-11\">Perform groupings</h3>\n  </div>\n\n  <!-- Button for adding groupings -->\n  <div class=\"row\">\n    <button class=\"btn btn-primary dq-btn-edit-grouping col-xs-offset-1\">Edit Grouping</button>\n  </div>\n\n  <!-- The grouping is displayed this header -->\n  <div class=\"dq-grouping-section-container\">\n    <h4 class=\"row col-xs-offset-1 dq-grouping-text\">No Groupings...</h4>\n  </div>\n\n  <!-- Section 4: Sorting -->\n  <div class=\"row dq-section\">\n    <div class=\"dq-circle hidden-xs col-sm-1\">4</div>\n    <h3 class=\"dq-title col-xs-11\">Sort by column</h3>\n  </div>\n\n  <!-- Button to add a sorting -->\n  <div class=\"row\">\n    <button class=\"btn btn-primary dq-btn-edit-sorting col-xs-offset-1\">Edit Sorting</button>\n  </div>\n\n  <!-- The sorting is displayed in this header -->\n  <div class=\"dq-sorting-section-container\">\n    <h4 class=\"row col-xs-offset-1 dq-sorting-text\">No Sorting...</h4>\n  </div>\n\n  <!-- Button to run query -->\n  <div class=\"row\">\n    <button class=\"btn btn-warning col-xs-3 col-xs-offset-3 dq-btn-cancel-query\">Cancel</button>\n    <button class=\"btn btn-success col-xs-3 dq-btn-run-query\">Query</button>\n  </div>\n</div>\n";
  },"useData":true});
this["DataQ"]["templates"]["dq-filter-list-item"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "<!-- HTML for filter in list of filters displayed in main DataQ container -->\n<li class=\"dq-filter-list-item\">\n  <div class=\"btn-group\" role=\"group\" aria-label=\"...\" data-code=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.filter : depth0)) != null ? stack1.code : stack1), depth0))
    + "\">\n\n    <!-- Button to delete filter -->\n    <button type=\"button\" class=\"btn btn-danger btn-mini dq-btn-delete-filter\">\n      <span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span>\n    </button>\n\n    <!-- The filter text content -->\n    <button type=\"button\" class=\"btn btn-default dq-filter-name\" ><span>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.filter : depth0)) != null ? stack1.filter_string : stack1), depth0))
    + "</span></button>\n  </div>\n</li>\n";
},"useData":true});
this["DataQ"]["templates"]["dq-filter-modal"] = Handlebars.template({"1":function(depth0,helpers,partials,data,depths) {
  var lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "              <li><a href=\"#\" class=\"dq-filter-1-link\" data-columnname=\""
    + escapeExpression(lambda((depth0 != null ? depth0.column_name : depth0), depth0))
    + "\" data-reponame=\""
    + escapeExpression(lambda((depths[1] != null ? depths[1].repo : depths[1]), depth0))
    + "\" data-tablename=\""
    + escapeExpression(lambda((depth0 != null ? depth0.table_name : depth0), depth0))
    + "\">"
    + escapeExpression(lambda((depth0 != null ? depth0.full_name : depth0), depth0))
    + "</a></li>\n";
},"3":function(depth0,helpers,partials,data,depths) {
  var lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "              <li><a href=\"#\" class=\"dq-filter-2-link\" data-columnname=\""
    + escapeExpression(lambda((depth0 != null ? depth0.column_name : depth0), depth0))
    + "\" data-reponame=\""
    + escapeExpression(lambda((depths[1] != null ? depths[1].repo : depths[1]), depth0))
    + "\" data-tablename=\""
    + escapeExpression(lambda((depth0 != null ? depth0.table_name : depth0), depth0))
    + "\">"
    + escapeExpression(lambda((depth0 != null ? depth0.full_name : depth0), depth0))
    + "</a></li>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
  var stack1, buffer = "<!-- Modal HTML for adding a filter -->\n<div class=\"modal fade\" id=\"dq-filter-modal\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <button type=\"button\" class=\"close dq-filter-quit\" data-dismiss=\"modal\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>\n\n        <!-- Title indicating that this modal is for creating filters -->\n        <h4 class=\"modal-title\">Create a Filter</h4>\n      </div>\n\n      <!-- Modal body -->\n      <div class=\"modal-body row form-inline filter-modal-body\">\n\n        <!-- The first dropdown where the user can specify <val1> in the filter <val1> <operation> <val2> -->\n        <div class=\"input-group col-xs-4\">\n          <!-- Text box for entering the filter text -->\n          <input type=\"text\" class=\"form-control dq-filter-1-text\" placeholder=\"table1.col1 * 3\">\n          <!-- Dropdown for selecting a column to add to filter -->\n          <div class=\"input-group-btn\">\n            <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\" aria-expanded=\"false\"><span class=\"caret\"></span></button>\n            <ul class=\"dropdown-menu dropdown-menu-right\" role=\"menu\">\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.columns : depth0), {"name":"each","hash":{},"fn":this.program(1, data, depths),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </ul>\n          </div>\n        </div> <!-- end filter1 -->\n\n        <!-- The first dropdown where the user can specify <operation> in the filter <val1> <operation> <val2> -->\n        <div class=\"input-group col-xs-3\">\n          <!-- Text box for entering the operation text -->\n          <input type=\"text\" class=\"form-control dq-filter-op-text\" placeholder=\"=\">\n          <!-- The possible operations are <, <=, >, >=, =, LIKE, IN, and NOT IN -->\n          <div class=\"input-group-btn\">\n            <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\" aria-expanded=\"false\"><span class=\"caret\"></span></button>\n            <ul class=\"dropdown-menu dropdown-menu-right\" role=\"menu\">\n              <li><a href=\"#\" class=\"dq-filter-op-link\">&lt</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">&lt=</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">=</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">&gt</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">&gt=</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">LIKE</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">IN</a></li>\n              <li><a href=\"#\" class=\"dq-filter-op-link\">NOT IN</a></li>\n            </ul>\n          </div>\n        </div> <!-- end filterop -->\n\n        <!-- The first dropdown where the user can specify <val2> in the filter <val1> <operation> <val2> -->\n        <div class=\"input-group col-xs-4\">\n          <!-- Text box for entering the filter text -->\n          <input type=\"text\" class=\"form-control dq-filter-2-text\" placeholder=\"table2.col2+3\">\n          <!-- Dropdown for selecting a column to add to filter -->\n          <div class=\"input-group-btn\">\n            <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\" aria-expanded=\"false\"><span class=\"caret\"></span></button>\n            <ul class=\"dropdown-menu dropdown-menu-right\" role=\"menu\">\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.columns : depth0), {"name":"each","hash":{},"fn":this.program(3, data, depths),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            </ul>\n          </div>\n        </div> <!-- end filter2 -->\n\n        <!-- Button to create filter -->\n        <div class=\"modal-footer\">\n          <button type=\"button\" class=\"btn btn-primary dq-filter-done\">Done</button>\n        </div>\n\n    </div><!-- /.modal-content -->\n  </div><!-- /.modal-dialog -->\n</div><!-- /.modal -->\n\n";
},"useData":true,"useDepths":true});
this["DataQ"]["templates"]["dq-grouping-modal"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "            <li class=\"dq-grouping-list-item sortable-placeholder\"\n              data-table=\""
    + escapeExpression(lambda((depth0 != null ? depth0.table : depth0), depth0))
    + "\"\n              data-column_name=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.column : depth0)) != null ? stack1.name : stack1), depth0))
    + "\"\n              data-column_type=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.column : depth0)) != null ? stack1.type : stack1), depth0))
    + "\"\n              data-column_agg=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.column : depth0)) != null ? stack1.agg : stack1), depth0))
    + "\"\n              data-string=\""
    + escapeExpression(lambda((depth0 != null ? depth0.string : depth0), depth0))
    + "\">\n              <button class=\"btn btn-default\" disabled>"
    + escapeExpression(lambda((depth0 != null ? depth0.string : depth0), depth0))
    + "</button>\n            </li>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"modal fade\" id=\"dq-grouping-modal\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <button id=\"dq-grouping-modal-quit-btn\" type=\"button\" class=\"close\" data-dismiss=\"modal\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>\n          <h4 class=\"modal-title\">Drag/Drop to Update Grouping.</h4>\n      </div>\n      <div class=\"modal-body\">\n        <ul class=\"dq-grouping-modal-list sortable\">\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.columns : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        </ul>\n      </div>\n      <div class=\"modal-footer\">\n        <button id=\"dq-grouping-modal-done-btn\" type=\"button\" class=\"btn btn-primary\" data-dismiss=\"modal\">Done</button>\n      </div>\n    </div><!-- /.modal-content -->\n  </div><!-- /.modal-dialog -->\n</div><!-- /.modal -->\n\n";
},"useData":true});
this["DataQ"]["templates"]["dq-modal-columns"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "<li class=\"dq-modal-column\" data-columnname="
    + escapeExpression(lambda((depth0 != null ? depth0['0'] : depth0), depth0))
    + " data-columntype="
    + escapeExpression(lambda((depth0 != null ? depth0['1'] : depth0), depth0))
    + " data-currentaggregate=\"none\">\n  <!-- Display a checkbox and a button (to toggle the aggregate operator) -->\n  <input type=\"checkbox\">\n  <button class=\"btn btn-default\">"
    + escapeExpression(lambda((depth0 != null ? depth0['0'] : depth0), depth0))
    + "</button>\n</li>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<!-- Create list of columns in the given table. This is used by the table modal -->\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.columns : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
this["DataQ"]["templates"]["dq-modal-dropdown-item"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<!-- List item in a dropdown. It is used by the sort group list -->\n<li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\" class=\"dq-modal-dropdown-link\" data-item_name=\""
    + escapeExpression(((helper = (helper = helpers.item_name || (depth0 != null ? depth0.item_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"item_name","hash":{},"data":data}) : helper)))
    + "\">"
    + escapeExpression(((helper = (helper = helpers.item_name || (depth0 != null ? depth0.item_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"item_name","hash":{},"data":data}) : helper)))
    + "</a></li>\n";
},"useData":true});
this["DataQ"]["templates"]["dq-selected-table"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<!-- Display a selected table in the main DataQ container -->\n<div class=\"row dq-contains-table-"
    + escapeExpression(((helper = (helper = helpers.table_name || (depth0 != null ? depth0.table_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"table_name","hash":{},"data":data}) : helper)))
    + "\" >\n  <ul class=\"dq-table-list col-xs-12\">\n    <li class=\"col-xs-10\">\n\n      <!-- Button for deleting -->\n      <div class=\"btn-group row\" role=\"group\" aria-label=\"...\">\n        <button type=\"button\" class=\"btn btn-danger btn-mini dq-btn-delete-table\" data-tablename=\""
    + escapeExpression(((helper = (helper = helpers.table_name || (depth0 != null ? depth0.table_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"table_name","hash":{},"data":data}) : helper)))
    + "\">\n          <span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span>\n        </button>\n        <!-- Button for editing -->\n        <button type=\"button\" class=\"btn btn-warning btn-mini dq-btn-edit-table\" data-tablename=\""
    + escapeExpression(((helper = (helper = helpers.table_name || (depth0 != null ? depth0.table_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"table_name","hash":{},"data":data}) : helper)))
    + "\">\n          <span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span>\n        </button>\n\n        <!-- Table name -->\n        <button type=\"button\" class=\"btn btn-default dq-table-name\" disabled>"
    + escapeExpression(((helper = (helper = helpers.table_name || (depth0 != null ? depth0.table_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"table_name","hash":{},"data":data}) : helper)))
    + "</button>\n      </div>\n\n      <!-- Columns in the table -->\n      <span class=\"row dq-columns\">"
    + escapeExpression(((helper = (helper = helpers.column_list || (depth0 != null ? depth0.column_list : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"column_list","hash":{},"data":data}) : helper)))
    + "</span>\n    </li>\n  </ul>\n</div>\n";
},"useData":true});
this["DataQ"]["templates"]["dq-sort-dropdown-li"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "<li>\n<a href=\"#\" class=\"dq-sort-link\" data-columnname=\""
    + escapeExpression(lambda(((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.column : stack1)) != null ? stack1.name : stack1), depth0))
    + "\" data-columntype=\""
    + escapeExpression(lambda(((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.column : stack1)) != null ? stack1.type : stack1), depth0))
    + "\" data-aggregate=\""
    + escapeExpression(lambda(((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.column : stack1)) != null ? stack1.agg : stack1), depth0))
    + "\" data-table=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.table : stack1), depth0))
    + "\" data-string=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.string : stack1), depth0))
    + "\">\n    "
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.string : stack1), depth0))
    + "\n  </a>\n</li>\n";
},"useData":true});
this["DataQ"]["templates"]["dq-sort-list-item"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "<li class=\"dq-sort-list-item\" data-columnname=\""
    + escapeExpression(lambda(((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.column : stack1)) != null ? stack1.name : stack1), depth0))
    + "\" data-columntype=\""
    + escapeExpression(lambda(((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.column : stack1)) != null ? stack1.type : stack1), depth0))
    + "\" data-aggregate=\""
    + escapeExpression(lambda(((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.column : stack1)) != null ? stack1.aggregate : stack1), depth0))
    + "\" data-table=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.table : stack1), depth0))
    + "\" data-string=\""
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.string : stack1), depth0))
    + "\">\n  <div class=\"btn-group\" role=\"group\" aria-label=\"...\"> \n    <button type=\"button\" class=\"btn btn-danger btn-mini dq-sort-delete-btn\">\n      <span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span>\n    </button>\n    <button type=\"button\" class=\"btn btn-default\" disabled><span>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.string : stack1), depth0))
    + "</span></button>\n  </div>\n</li>\n";
},"useData":true});
this["DataQ"]["templates"]["dq-sort-modal"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"modal fade\" id=\"dq-sort-modal\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <button type=\"button\" class=\"close dq-sort-modal-quit\" data-dismiss=\"modal\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>\n        <h4 class=\"modal-title\">Pick Columns to Sort By</h4>\n      </div>\n      <div class=\"modal-body\">\n        <div class=\"dropdown\">\n          <button class=\"btn btn-default dropdown-toggle dq-sort-modal-dropdown-btn\" type=\"button\" id=\"dropdownMenu1\" data-toggle=\"dropdown\" aria-expanded=\"true\">\n            <span class=\"dq-modal-sort-dropdown-text\">Select Sort Column...</span>\n            <span class=\"caret\"></span>\n          </button>\n          <ul class=\"dropdown-menu dq-sort-modal-dropdown\" role=\"menu\" aria-labelledby=\"dropdownMenu1\">\n          </ul>\n        </div>\n        <ul class=\"dq-sort-item-list\">\n        </ul>\n      </div>\n      <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-primary dq-sort-modal-done-btn\" data-dismiss=\"modal\">Done</button>\n      </div>\n    </div><!-- /.modal-content -->\n  </div><!-- /.modal-dialog -->\n</div><!-- /.modal -->\n";
  },"useData":true});
this["DataQ"]["templates"]["dq-table-modal"] = Handlebars.template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "          <h4 class=\"modal-title\">Update Columns in "
    + escapeExpression(((helper = (helper = helpers.table_name || (depth0 != null ? depth0.table_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"table_name","hash":{},"data":data}) : helper)))
    + "</h4>\n";
},"3":function(depth0,helpers,partials,data) {
  return "          <h4 class=\"modal-title\">Add Table and Select Columns</h4>\n";
  },"5":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "          <span class=\"dq-modal-table-name\">Table: "
    + escapeExpression(((helper = (helper = helpers.table_name || (depth0 != null ? depth0.table_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"table_name","hash":{},"data":data}) : helper)))
    + "</span>\n";
},"7":function(depth0,helpers,partials,data) {
  return "        <div class=\"dropdown\">\n          <button class=\"btn btn-default dropdown-toggle dq-modal-dropdown-btn\" type=\"button\" id=\"dropdownMenu1\" data-toggle=\"dropdown\" aria-expanded=\"true\">\n            <span class=\"dq-modal-table-dropdown-text\">Select Table...</span>\n            <span class=\"caret\"></span>\n          </button>\n          <ul class=\"dropdown-menu dq-modal-dropdown\" role=\"menu\" aria-labelledby=\"dropdownMenu1\"></ul>\n        </div>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"modal fade\" id=\"dq-table-modal\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <button type=\"button\" class=\"close dq-modal-quit\" data-dismiss=\"modal\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.table_name : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "      </div>\n      <div class=\"modal-body\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.table_name : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.program(7, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        <ul class=\"dq-column-list\">\n        </ul>\n      </div>\n      <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-primary dq-modal-done-btn\" data-dismiss=\"modal\">Done</button>\n      </div>\n    </div><!-- /.modal-content -->\n  </div><!-- /.modal-dialog -->\n</div><!-- /.modal -->\n";
},"useData":true});
this["DataQ"]["templates"]["dq-table-section"] = Handlebars.template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div class=\"dq-selected-tables\">\n</div>\n<div class=\"row\">\n  <button class=\"btn btn-primary dq-btn-add-table col-xs-offset-1\">Add Table</button>\n</div>\n";
  },"useData":true});