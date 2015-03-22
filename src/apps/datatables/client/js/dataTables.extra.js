(function($) {
  var url_base = "/apps/datatables/api/";
  $.fn.EnhancedDataTable = function(repo, table) {
    var url_table = url_base + "table/" + repo + "/" + table + "/";
    var url_schema = url_base + "schema/" + repo + "/" + table + "/";
    var thisDataTable = this;

    // First get the schema so we can set the column names.
    $.get(url_schema, function(schema_result) {
      if (schema_result.success) { // Was the schema retrieved successfully?

        // Create the column definitions to put into the data table.
        var columnDefinitions = [];
        var schema = schema_result.schema;
        for (var i = 0; i < schema.length; i++) {
          columnDefinitions.push({
            "name": schema[i][0],
            "targets": i
          });
        }
        
        // Add buttons to add filters.
        var buttonHtml ='<div class="input-group">'
        + '<span class="input-group-btn">'
        + '<button class="btn btn-default dt-bool-button" type="button">OR</button>'
        + '</span>'
        + '<input type="text" class="form-control" placeholder="Filter...">'
        + '<span class="input-group-btn">'
        + '<button class="btn btn-default dt-op-button" type="button">=</button>'
        + '</span>'
        + '</div>';

        var singleEndButtonHtml ='<div class="input-group">'
        + '<input type="text" class="form-control" placeholder="Filter...">'
        + '<span class="input-group-btn">'
        + '<button class="btn btn-default dt-op-button" type="button">=</button>'
        + '</span>'
        + '</div>';

        thisDataTable.find('tfoot th').each(function(index) {
          var title = thisDataTable.find('thead th').eq( $(this).index() ).text();
          $(this).attr("data-colname", title);
          console.log(title);
          if (index > 0) {
            $(this).append(buttonHtml);
          } else {
            $(this).append(singleEndButtonHtml);
          }
        });

        $(document).on("click", ".dt-bool-button", function() {
          if ($(this).text() == "AND") {
            $(this).text("OR");
          } else {
            $(this).text("AND");
          }
        }); 

        var nextOp = {
          "=": "not=",
          "not=": "<",
          "<": "<=",
          "<=": ">",
          ">": ">=",
          ">=": "="
        };

        $(document).on("click", ".dt-op-button", function() {
          $(this).text(nextOp[$(this).text()]);
        });
             
        thisDataTable.DataTable({
          "columnDefs": columnDefinitions,
          "searching": false,
          "scrollX": true,
          "serverSide": true,
          "ajax": {
            "url": "/apps/datatables/api/table/" + repo + "/" + table + "/",
            "data": function(d) {
            }
          }
        });
      } else {
        alert("failed to load table");
      }
    });
    return this;
  };
})(jQuery);
