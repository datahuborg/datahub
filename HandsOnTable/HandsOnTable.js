// var startRepo = listRepos().tuples[0].cells[0];
// var options = listRepos().tuples;
// var tempRepoName = null;
// //var repoName = startRepo.slice();
// var tempURL = document.location.pathname.split('index.html')[1]
var repoName = "test";
var fullTableName = "";
var dataTypes = ['bigint', 'bit', 'decimal', 'int', 'money', 'numeric', 'smallint', 'smallmoney', 'tinyint', 'float', 'real', 'date', 'datetime2', 'datetime', 'datetimeoffset', 'smalldatetime', 'time',
                'char', 'text', 'varchar', 'nchar', 'ntext', 'nvarchar', 'binary', 'image', 'varbinary', 'cursor', 'hierarchyid', 'sql_variant', 'table', 'timestamp', 'uniqueidentifier', 'xml'];
var numberTypes = ["bigint", "bit", "decimal", "int", "integer", "money", "numeric", "smallint", "smallmoney", "tinyint", "float", "real", "double", "double precision"]
var decimalTypes = ["decimal", "money", "numeric", "smallmoney", "float", "real", "double", "double precision"]

// $(window).bind('setup', function() {
//    if (repoName == null) {
//         $("#popUpDiv").show();
//     }
//     $("#popupSelect").change(function(e) {
//         repoName = $("#popupSelect").val();
//         $("#popUpDiv").hide();
//     });
// });
var Handsontable_deferred = $.Deferred();

// Display after authoirzation granted
Handsontable_deferred.done(function() {
    var listOfRepos = document.getElementById('selectRepo');

  if (document.location.pathname.indexOf("/chooseRepo.html") != -1) {
    for(var i = 0; i < options.length; i++) {
      var opt = options[i].cells[0];
      var el = document.createElement("option");
      el.textContent = opt;
      el.value = opt;
      listOfRepos.appendChild(el);
    }

    $(document).on('change', '#selectRepo',function(){
      tempRepoName = $(this).val();
      var listOfTables = document.getElementById('selectTable');
      var tableOptions = client.list_tables(con, tempRepoName).tuples;

      $('#selectTable').empty();
      var prompt = document.createElement("option");
      prompt.textContent = "Select a Table";
      prompt.value = "";
      prompt.disabled;
      listOfTables.appendChild(prompt);

      for(var i = 0; i < tableOptions.length; i++) {
        var opt = tableOptions[i].cells[0];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        listOfTables.appendChild(el);
      }
    });

    $(document).on('click', '#select', function() {
      repoName = $('#selectRepo').val();
      tableName = $('#selectTable').val();
      fullTableName = accountName+ '.'+repoName+ '.'+tableName;
      alert("selected repo and table: "+ repoName+", "+fullTableName);
// /'repoName+'/'+tableName
      window.location.href = './index.html';
      // $.get( "./index.html", function( data ) {
      //   $( ".fullTableName" ).html( fullTableName );
      //   alert( "Load was performed." );
      // });
    });
  };
  // document.location.pathname.indexOf("/chooseRepo.html") != -1

  // if (!repoName) {
  //   repoNames = listRepos().tuples.map(function (tuple) { return tuple.cells[0]; });
  //   repoName = prompt("Enter the name of the repo you'd like to edit: \n\n"+ repoNames.join("\n"),"testRepo");
  // }
    // handle error banner
  // if (document.location.pathname.indexOf("/index.html") != -1) {
  if (true) {
    var displayErrorMessage = function (errorMsg, errorSubMsg) {
          $('#error_msg').text(errorMsg);
          $('#error_submsg').text((errorSubMsg ? errorSubMsg : 'No more information about this error.'));
          $('#error_alert').show();
      }
      $('.alert .close').on('click', function(e) {
          $(this).parent().hide();
      });

      repos = listRepos();
      var unsavedData = [];

      chart_client = charts(accountName, client, con);
      $('#chart_menu').click(chart_client.openModal);

      $('#results').handsontable({
      minSpareRows: 1,
          //manualColumnMove: true, // COLUMN ORDERING IN VIEW NOT ACCESSIBLE IN 0.15.2 HANDSONTABLE
          //manualRowMove: true, // MESSES UP SAVING BY ROW
          manualColumnResize: true,
          manualRowResize: true,
          columnSorting: true,
          rowHeaders: true,
          persistentState: true,
      contextMenu: ['remove_col', 'row_above', 'row_below', 'col_left', 'col_right', 'remove_row'],
          cells: function(row, col, prop) {
              this.renderer = function (instance, td, row, col, prop, value, cellProperties) {
                  value = (value === "None" ? '' : value);
                  if (cellProperties.type === 'numeric') {
                      Handsontable.renderers.NumericRenderer.apply(this, arguments);
                  } else if (cellProperties.type === 'password') {
                      Handsontable.renderers.PasswordRenderer.apply(this, arguments);
                  } else if (cellProperties.type === 'autocomplete') {
                      Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
                  } else if (cellProperties.type === 'checkbox') {
                      Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
                  } else {
                      Handsontable.renderers.TextRenderer.apply(this, arguments);
                  }
                  if (cellProperties.unsaved === 'true') {
                      td.style.background = 'yellow';
                  } else {
                      td.style.background = 'white';
                  }
              };
          }
    });
      // Code for autosaving changes, can be uncommented for functionality
      // $('#results').handsontable('getInstance').addHook('afterChange', function (changes, source) {
      //     if (!changes || source !== 'edit') { return; }
      //     var hot = this;
      //     $.each(changes, function (index, element) {
      //         var p_key = hot.getDataAtCell(element[0], getPKColNum(hot));
      //         var field_name = hot.getColHeader(element[1]);
      //         var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[element[0]][0] : element[0];
      //         var new_val = hot.getCellMeta(cellRow ,element[1]).type === 'numeric' ? element[3] : "'" + element[3] + "'";
      //         new_val = new_val === '' ?  '0' : new_val;

      //         executeSQL(buildUpdateQuery(fullTableName, { field_name: new_val }, p_key), function (res) {
      //             // TODO (jennya)
      //             return;
      //         }, function (err) {
      //             // TODO (jennya)
      //             return;
      //         });
      //     });
      // });
      $('#results').handsontable('getInstance').addHook('afterRemoveCol', function (index, amount) {
          for (var i = index; i < index + amount; i++) {
              var colHeader = this.getColHeader(i);
              executeSQL(buildSelectQuery(fullTableName, [colHeader], 0), function (res) {
                  getViewFields(fullTableName + '_view', function (fields_set) {
                      fieldName = fullTableName.slice(fullTableName.lastIndexOf('.') + 1) + '.' + colHeader;
                      delete fields_set[fieldName];
                      replaceView(fullTableName + '_view', fields_set);
                      executeSQL(buildDropColumnQuery(fullTableName, colHeader, true), function (res) {
                          // silent on success -- view changes to show column removed
                          return;
                      }, function (err) {
                          displayErrorMessage('Unable to remove column "' + colHeader + '"', err.message);
                          return;
                      });
                  }); 
              }, function (err) {
                  removeColFromView(fullTableName + '_view', colHeader);
              });
          }
      });
      $('#results').handsontable('getInstance').addHook('beforeChange', function (changes, source) {
          // Add changes to unsaved data and highlight the edited cell
          var hot = this;
          $.each(changes, function (index, change) {
              console.log(change);
              var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[change[0]][0] : change[0];
              hot.setCellMeta(cellRow, change[1], 'unsaved', 'true');
              unsavedData.push([change[0], hot.getSettings().colHeaders[change[1]]]);
          });
      });
      $('#results').handsontable('getInstance').addHook('beforeRemoveCol', function (index, amount) {
          // Don't allow a user to remove the p_key column
          pKeyCol = getPKColNum(this);
          if (pKeyCol >= index && pKeyCol < index + amount) {
              // error handle before returning false so the column isn't removed
              displayErrorMessage('Can\'t delete the primary key column');
              return false;
          }
      });
      $('#results').handsontable('getInstance').addHook('beforeKeyDown', function (event) {
          // Check if the key is '=', if it is, then enter the equation environment
          var hot = this;
          var selectedRange = hot.getSelected();
          var td = $(hot.getCell(selectedRange[0], selectedRange[1]));
          // if the equals key is pressed, enter the equation environment
          if (event.key === '=') {
              var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[selectedRange[0]][0] : selectedRange[0];
              hot.setCellMeta(cellRow, selectedRange[1], 'type', 'text');
              var div = document.createElement('div');
              div.style.left = td.offset().left;
              div.style.top = td.offset().top + td.height() + 5;
              div.style.height = td.height();
              div.style.position = 'absolute';
              div.style.backgroundColor = '#e7e7e7';
              div.className = 'editButtons';

              var checkbtn = document.createElement('button');
              var xbtn = document.createElement('button');
              checkbtn.className = "btn btn-default";
              xbtn.className = "btn btn-default";
              checkbtn.onclick = function (e) {
                  // evaluate formula for all highlighted cells
                  $('.editButtons').remove();
                  var col_header = hot.getColHeader(selectedRange[1]);
                  if (col_header !== 'p_key') {
                      addColToView(fullTableName + '_view', hot.getDataAtCell(selectedRange[0], selectedRange[1]).substr(1), col_header);
                      
                      // remove old column
                      executeSQL(buildDropColumnQuery(fullTableName, col_header, true), function (res) {
                          refreshCellMeta(fullTableName);
                      }, function (err) {
                          displayErrorMessage('Could not delete column "' + col_header + '"', err.message);
                          return;
                      });
                  }
              };
              xbtn.onclick = function () {
                  hot.undo();
                  $('.editButtons').remove();
              }
              $(checkbtn).html('<span class="glyphicon glyphicon-ok"></span>');
              $(xbtn).html('<span class="glyphicon glyphicon-remove"></span>');
              div.appendChild(xbtn);
              div.appendChild(checkbtn);
              document.body.appendChild(div);
          }
      });
      $('#results').handsontable('getInstance').addHook('afterCellMetaReset', function () {
          refreshCellMeta(fullTableName);
      });
      $('#results').handsontable('getInstance').addHook('afterCreateCol', function (index, amount) {
          $('#newColName').val('');
          $('#addColModal').modal();
      });
      $('#addColModal').find(".go_button").click(function() {
          if (dataTypes.indexOf($('#newColName').val()) > -1) {
              displayErrorMessage('Can\'t create a column with the name the same as a PostgreSQL data type');
              return;
          }
          // do the add col sql statement
          executeSQL(buildAddColumnQuery(fullTableName, $('#newColName').val(), $('#colTypes').val()), function (res) {
              refreshView(fullTableName + '_view');
          }, function (err) {
              displayErrorMessage('Could not add column ' + $('#newColName').val(), err.message);
              return;
          });
          
      });
      $(document).on('click', '#save', function() {
          console.log("SAVED CHANGES")
          // save all changes
          var hot = $('#results').handsontable('getInstance');
          // parse through unsaved data and orient it by row
          changesByRow = {};
          getColumnNames(fullTableName, function (realCols) {
              // Create a list of rows and for each row store an object 
              // with the fields that need to be updated
              $.each(unsavedData, function (index, data) {
                  var row = data[0];
                  var colHeader = data[1];
                  if (realCols.indexOf(colHeader) > -1) {
                      changesByRow[row] = changesByRow[row] === undefined ? {} : changesByRow[row];
                      changesByRow[row][colHeader] = true;
                  }
              });

              // Execute a SQL statement for each row, either create a new row or update an existing one
              var stmts = [];
              $.each(changesByRow, function (rowNum, changeObj) {
                  // see if rowNum has a p_key (if not we add a new row)
                  var p_key = hot.getDataAtCell(rowNum, getPKColNum(hot));
                  var sql = '';
                  if (p_key) {
                      // update row
                      changesObj = {};
                      $.each(changeObj, function (v, i) {
                          var field_name = v;
                          var changeCol = getColNum(hot, field_name);
                          var new_text = hot.getDataAtCell(rowNum, changeCol);
                          var new_val = hot.getCellMeta(rowNum, changeCol).type === 'numeric' ? new_text : "'" + new_text + "'";
                          new_val = new_val === '' || new_val === 'None' ?  '0' : new_val;
                          changesObj[field_name] = new_val;
                          rowNum = hot.sortIndex.length > 0 ? hot.sortIndex[rowNum][0] : rowNum;
                          hot.setCellMeta(rowNum, changeCol, 'unsaved', 'false'); 
                      });
                      sql = buildUpdateQuery(fullTableName, changesObj, p_key);
                  } else {
                      // create a new row
                      var fieldNames = [];
                      var newVals = [];
                      $.each(changeObj, function (v, i) {
                          var field_name = v;
                          var changeCol = getColNum(hot, field_name);
                          var new_text = hot.getDataAtCell(rowNum, changeCol);
                          var new_val = hot.getCellMeta(rowNum,changeCol).type === 'numeric' ? new_text : "'" + new_text + "'";
                          new_val = new_val === '' ?  '0' : new_val;
                          fieldNames.push(field_name);
                          newVals.push(new_val);
                          rowNum = hot.sortIndex.length > 0 ? hot.sortIndex[rowNum][0] : rowNum;
                          hot.setCellMeta(rowNum, changeCol, 'unsaved', 'false'); 
                      });
                      sql = buildInsertQuery(fullTableName, fieldNames, newVals);
                  }
                  stmts.push(sql);
              });
              console.log(stmts);
              $.each(stmts, function (index, sql) {
                  executeSQL(sql, function (res) {
                      // do nothing
                      return;
                  }, function (err) {
                      displayErrorMessage('Error in saving data.', err.message);
                      return;
                  });
              });
              unsavedData = [];
              updateTableData(fullTableName);
          });
      });

      // Returns the fields that are in the view including the formulas for computed columns
      // Returned as a dictionary of { fieldName: true }
      var getViewFields = function (viewName, callback) {
          executeSQL(buildGetViewDefQuery(viewName), function (res) {
              var sql = res.tuples[0].cells[0];
              sql = sql.slice(sql.indexOf('SELECT') + 7, sql.indexOf('FROM'));
              var fields = sql.split(',');
              var fields_set = {};
              $.each(fields, function (index, element) {
                  if (!fields_set[element.trim()]) {
                      fields_set[element.trim()] = true;
                  }
              });
              callback(fields_set);
          }, function (err) {
              displayErrorMessage('Could not retrieve columns in table.', err.message);
              return;
          });
          
      }

      // Sets the type of cell to reflect the type in DataHub
      // Make computed columns and p_key readOnly
      var refreshCellMeta = function (tableName) {
          var hot = $('#results').handsontable('getInstance');
          getColumnNames(tableName, function (realCols) {
              $.each(hot.getSettings().colHeaders, function (index, colData) {
                  var hasType = (realCols.indexOf(colData) > -1) ? true : false;
                  if (hasType) {
                      var dataType = getDataTypeForCol(colData);
                      var colDataType = { type: 'text' };
                      if (numberTypes.indexOf(dataType) > -1) {
                          // allowInvalid: false
                          colDataType = { type: 'numeric', format: '0,0[.]00' };
                      } else if (dataType === 'date') {
                          colDataType = { type: 'date', dateFormat: 'MM/DD/YYYY', correctFormat: true};
                      }
                  }
                  // run through all cells in col
                  for (var i = 0; i < hot.countRows(); i++) {
                      if (hasType) { 
                          $.each(Object.keys(colDataType), function (data_type_key_index, dataType) {
                              var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[i][0] : i;
                              hot.setCellMeta(cellRow, index, dataType, colDataType[dataType]);
                          });
                      }
                      if (colData === 'p_key' || !hasType) {
                          var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[i][0] : i;
                          hot.setCellMeta(cellRow, index, 'format', '0,0[.]00');
                          hot.setCellMeta(cellRow, index, 'type', 'numeric');
                          hot.setCellMeta(cellRow, index, 'readOnly', true);
                      } 
                  }
              });
              hot.render();
          });
      }

      // Adds a computed column to the view
      var addColToView = function (viewName, colExpr, colName) {
          getViewFields(viewName, function (fields_set) {
              tName = viewName.slice(viewName.lastIndexOf('.') + 1, viewName.indexOf('_view'));
              delete fields_set[tName + '.' + colName];
              fields_set['(' + colExpr + ') as ' + colName] = true;

              replaceView(viewName, fields_set);
          });
      }

      // Removes a column (computed or not) from the view
      var removeColFromView = function (viewName, colName) {
          getViewFields(viewName, function (fields_set) {
              var fieldToRemove = '';
              $.each(Object.keys(fields_set), function (index, key) {
                  if (key.substr(key.indexOf('AS') + 3) === colName) {
                      fieldToRemove = key;
                  }
              });
              delete fields_set[fieldToRemove];
              replaceView(viewName, fields_set);
          });
      }

      // Takes the current view and adds any columns present in the table to the view
      var refreshView = function (viewName) {
          var tName = viewName.slice(viewName.lastIndexOf('.') + 1, viewName.indexOf('_view'));
          getViewFields(viewName, function (fields_set) {
              getColumnNames(viewName.slice(0, viewName.indexOf('_view')), function (fieldNames) {
                  $.each(fieldNames, function (index, element) {
                      if (fields_set[element] === undefined) {
                          fields_set[tName + '.' + element] = true;
                      }
                  });
                  replaceView(viewName, fields_set);
              });
          });
      }

      // Drops the old view and creates a new one with the list of fields which are the keys in fields_set
      var replaceView = function (viewName, fields_set) {
          var new_cols = Object.keys(fields_set);
          // first drop existing view
          executeSQL(buildDropViewQuery(viewName, true), function (res) {
              // now create with new query
              executeSQL(buildCreateViewQuery(viewName, buildSelectQuery(viewName.slice(0, viewName.indexOf('_view')), new_cols)), function (res) {
                  updateTableData(viewName.slice(0, viewName.indexOf('_view')));
              }, function (err) {
                  displayErrorMessage('Could not create a new view.', err.message);
                  return;
              });
          }, function (err) {
              displayErrorMessage('Could not replace current view.', err.message);
              return;
          });
      }

      // Returns the index of the primary key column
      var getPKColNum = function (hot) {
          return getColNum(hot, 'p_key');
      }

      // Returns the index of the column with colName
      var getColNum = function (hot, colName) {
          for (var i = 0; i < hot.getSettings().colHeaders.length; i++) {
              if (hot.getColHeader(i) === colName) {
                  return i;
              }
          }
          return -1;
      }


      // prepare the add col modal
      $('#colTypes').select2({data: dataTypes });

      // Retrieve all data and populate the UI
      updateRepo(repoName);
  };

})

$('#interactive_part')
    .on('afterShow', function() {
//       alert('afterShow');
//     })
// $(document).ready(function () {
  var listOfRepos = document.getElementById('selectRepo');

  if (document.location.pathname.indexOf("/chooseRepo.html") != -1) {
    for(var i = 0; i < options.length; i++) {
      var opt = options[i].cells[0];
      var el = document.createElement("option");
      el.textContent = opt;
      el.value = opt;
      listOfRepos.appendChild(el);
    }

    $(document).on('change', '#selectRepo',function(){
      tempRepoName = $(this).val();
      var listOfTables = document.getElementById('selectTable');
      var tableOptions = client.list_tables(con, tempRepoName).tuples;

      $('#selectTable').empty();
      var prompt = document.createElement("option");
      prompt.textContent = "Select a Table";
      prompt.value = "";
      prompt.disabled;
      listOfTables.appendChild(prompt);

      for(var i = 0; i < tableOptions.length; i++) {
        var opt = tableOptions[i].cells[0];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        listOfTables.appendChild(el);
      }
    });

    $(document).on('click', '#select', function() {
      repoName = $('#selectRepo').val();
      tableName = $('#selectTable').val();
      fullTableName = accountName+ '.'+repoName+ '.'+tableName;
      alert("selected repo and table: "+ repoName+", "+fullTableName);
// /'repoName+'/'+tableName
      window.location.href = './index.html';
      // $.get( "./index.html", function( data ) {
      //   $( ".fullTableName" ).html( fullTableName );
      //   alert( "Load was performed." );
      // });
    });
  };
  // document.location.pathname.indexOf("/chooseRepo.html") != -1

  // if (!repoName) {
  //   repoNames = listRepos().tuples.map(function (tuple) { return tuple.cells[0]; });
  //   repoName = prompt("Enter the name of the repo you'd like to edit: \n\n"+ repoNames.join("\n"),"testRepo");
  // }
    // handle error banner
  if (document.location.pathname.indexOf("/index.html") != -1) {
  	var displayErrorMessage = function (errorMsg, errorSubMsg) {
          $('#error_msg').text(errorMsg);
          $('#error_submsg').text((errorSubMsg ? errorSubMsg : 'No more information about this error.'));
          $('#error_alert').show();
      }
      $('.alert .close').on('click', function(e) {
          $(this).parent().hide();
      });

      repos = listRepos();
      var unsavedData = [];

      chart_client = charts(accountName, client, con);
      $('#chart_menu').click(chart_client.openModal);

      $('#results').handsontable({
  		minSpareRows: 1,
          //manualColumnMove: true, // COLUMN ORDERING IN VIEW NOT ACCESSIBLE IN 0.15.2 HANDSONTABLE
          //manualRowMove: true, // MESSES UP SAVING BY ROW
          manualColumnResize: true,
          manualRowResize: true,
          columnSorting: true,
          rowHeaders: true,
          persistentState: true,
  		contextMenu: ['remove_col', 'row_above', 'row_below', 'col_left', 'col_right', 'remove_row'],
          cells: function(row, col, prop) {
              this.renderer = function (instance, td, row, col, prop, value, cellProperties) {
                  value = (value === "None" ? '' : value);
                  if (cellProperties.type === 'numeric') {
                      Handsontable.renderers.NumericRenderer.apply(this, arguments);
                  } else if (cellProperties.type === 'password') {
                      Handsontable.renderers.PasswordRenderer.apply(this, arguments);
                  } else if (cellProperties.type === 'autocomplete') {
                      Handsontable.renderers.AutocompleteRenderer.apply(this, arguments);
                  } else if (cellProperties.type === 'checkbox') {
                      Handsontable.renderers.CheckboxRenderer.apply(this, arguments);
                  } else {
                      Handsontable.renderers.TextRenderer.apply(this, arguments);
                  }
                  if (cellProperties.unsaved === 'true') {
                      td.style.background = 'yellow';
                  } else {
                      td.style.background = 'white';
                  }
              };
          }
  	});
      // Code for autosaving changes, can be uncommented for functionality
      // $('#results').handsontable('getInstance').addHook('afterChange', function (changes, source) {
      //     if (!changes || source !== 'edit') { return; }
      //     var hot = this;
      //     $.each(changes, function (index, element) {
      //         var p_key = hot.getDataAtCell(element[0], getPKColNum(hot));
      //         var field_name = hot.getColHeader(element[1]);
      //         var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[element[0]][0] : element[0];
      //         var new_val = hot.getCellMeta(cellRow ,element[1]).type === 'numeric' ? element[3] : "'" + element[3] + "'";
      //         new_val = new_val === '' ?  '0' : new_val;

      //         executeSQL(buildUpdateQuery(fullTableName, { field_name: new_val }, p_key), function (res) {
      //             // TODO (jennya)
      //             return;
      //         }, function (err) {
      //             // TODO (jennya)
      //             return;
      //         });
      //     });
      // });
      $('#results').handsontable('getInstance').addHook('afterRemoveCol', function (index, amount) {
          for (var i = index; i < index + amount; i++) {
              var colHeader = this.getColHeader(i);
              executeSQL(buildSelectQuery(fullTableName, [colHeader], 0), function (res) {
                  getViewFields(fullTableName + '_view', function (fields_set) {
                      fieldName = fullTableName.slice(fullTableName.lastIndexOf('.') + 1) + '.' + colHeader;
                      delete fields_set[fieldName];
                      replaceView(fullTableName + '_view', fields_set);
                      executeSQL(buildDropColumnQuery(fullTableName, colHeader, true), function (res) {
                          // silent on success -- view changes to show column removed
                          return;
                      }, function (err) {
                          displayErrorMessage('Unable to remove column "' + colHeader + '"', err.message);
                          return;
                      });
                  }); 
              }, function (err) {
                  removeColFromView(fullTableName + '_view', colHeader);
              });
          }
      });
      $('#results').handsontable('getInstance').addHook('beforeChange', function (changes, source) {
          // Add changes to unsaved data and highlight the edited cell
          var hot = this;
          $.each(changes, function (index, change) {
              console.log(change);
              var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[change[0]][0] : change[0];
              hot.setCellMeta(cellRow, change[1], 'unsaved', 'true');
              unsavedData.push([change[0], hot.getSettings().colHeaders[change[1]]]);
          });
      });
      $('#results').handsontable('getInstance').addHook('beforeRemoveCol', function (index, amount) {
          // Don't allow a user to remove the p_key column
          pKeyCol = getPKColNum(this);
          if (pKeyCol >= index && pKeyCol < index + amount) {
              // error handle before returning false so the column isn't removed
              displayErrorMessage('Can\'t delete the primary key column');
              return false;
          }
      });
      $('#results').handsontable('getInstance').addHook('beforeKeyDown', function (event) {
          // Check if the key is '=', if it is, then enter the equation environment
          var hot = this;
          var selectedRange = hot.getSelected();
          var td = $(hot.getCell(selectedRange[0], selectedRange[1]));
          // if the equals key is pressed, enter the equation environment
          if (event.key === '=') {
              var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[selectedRange[0]][0] : selectedRange[0];
              hot.setCellMeta(cellRow, selectedRange[1], 'type', 'text');
              var div = document.createElement('div');
              div.style.left = td.offset().left;
              div.style.top = td.offset().top + td.height() + 5;
              div.style.height = td.height();
              div.style.position = 'absolute';
              div.style.backgroundColor = '#e7e7e7';
              div.className = 'editButtons';

              var checkbtn = document.createElement('button');
              var xbtn = document.createElement('button');
              checkbtn.className = "btn btn-default";
              xbtn.className = "btn btn-default";
              checkbtn.onclick = function (e) {
                  // evaluate formula for all highlighted cells
                  $('.editButtons').remove();
                  var col_header = hot.getColHeader(selectedRange[1]);
                  if (col_header !== 'p_key') {
                      addColToView(fullTableName + '_view', hot.getDataAtCell(selectedRange[0], selectedRange[1]).substr(1), col_header);
                      
                      // remove old column
                      executeSQL(buildDropColumnQuery(fullTableName, col_header, true), function (res) {
                          refreshCellMeta(fullTableName);
                      }, function (err) {
                          displayErrorMessage('Could not delete column "' + col_header + '"', err.message);
                          return;
                      });
                  }
              };
              xbtn.onclick = function () {
                  hot.undo();
                  $('.editButtons').remove();
              }
              $(checkbtn).html('<span class="glyphicon glyphicon-ok"></span>');
              $(xbtn).html('<span class="glyphicon glyphicon-remove"></span>');
              div.appendChild(xbtn);
              div.appendChild(checkbtn);
              document.body.appendChild(div);
          }
      });
      $('#results').handsontable('getInstance').addHook('afterCellMetaReset', function () {
          refreshCellMeta(fullTableName);
      });
      $('#results').handsontable('getInstance').addHook('afterCreateCol', function (index, amount) {
          $('#newColName').val('');
          $('#addColModal').modal();
      });
      $('#addColModal').find(".go_button").click(function() {
          if (dataTypes.indexOf($('#newColName').val()) > -1) {
              displayErrorMessage('Can\'t create a column with the name the same as a PostgreSQL data type');
              return;
          }
          // do the add col sql statement
          executeSQL(buildAddColumnQuery(fullTableName, $('#newColName').val(), $('#colTypes').val()), function (res) {
              refreshView(fullTableName + '_view');
          }, function (err) {
              displayErrorMessage('Could not add column ' + $('#newColName').val(), err.message);
              return;
          });
          
      });
      $(document).on('click', '#save', function() {
          console.log("SAVED CHANGES")
          // save all changes
          var hot = $('#results').handsontable('getInstance');
          // parse through unsaved data and orient it by row
          changesByRow = {};
          getColumnNames(fullTableName, function (realCols) {
              // Create a list of rows and for each row store an object 
              // with the fields that need to be updated
              $.each(unsavedData, function (index, data) {
                  var row = data[0];
                  var colHeader = data[1];
                  if (realCols.indexOf(colHeader) > -1) {
                      changesByRow[row] = changesByRow[row] === undefined ? {} : changesByRow[row];
                      changesByRow[row][colHeader] = true;
                  }
              });

              // Execute a SQL statement for each row, either create a new row or update an existing one
              var stmts = [];
              $.each(changesByRow, function (rowNum, changeObj) {
                  // see if rowNum has a p_key (if not we add a new row)
                  var p_key = hot.getDataAtCell(rowNum, getPKColNum(hot));
                  var sql = '';
                  if (p_key) {
                      // update row
                      changesObj = {};
                      $.each(changeObj, function (v, i) {
                          var field_name = v;
                          var changeCol = getColNum(hot, field_name);
                          var new_text = hot.getDataAtCell(rowNum, changeCol);
                          var new_val = hot.getCellMeta(rowNum, changeCol).type === 'numeric' ? new_text : "'" + new_text + "'";
                          new_val = new_val === '' || new_val === 'None' ?  '0' : new_val;
                          changesObj[field_name] = new_val;
                          rowNum = hot.sortIndex.length > 0 ? hot.sortIndex[rowNum][0] : rowNum;
                          hot.setCellMeta(rowNum, changeCol, 'unsaved', 'false'); 
                      });
                      sql = buildUpdateQuery(fullTableName, changesObj, p_key);
                  } else {
                      // create a new row
                      var fieldNames = [];
                      var newVals = [];
                      $.each(changeObj, function (v, i) {
                          var field_name = v;
                          var changeCol = getColNum(hot, field_name);
                          var new_text = hot.getDataAtCell(rowNum, changeCol);
                          var new_val = hot.getCellMeta(rowNum,changeCol).type === 'numeric' ? new_text : "'" + new_text + "'";
                          new_val = new_val === '' ?  '0' : new_val;
                          fieldNames.push(field_name);
                          newVals.push(new_val);
                          rowNum = hot.sortIndex.length > 0 ? hot.sortIndex[rowNum][0] : rowNum;
                          hot.setCellMeta(rowNum, changeCol, 'unsaved', 'false'); 
                      });
                      sql = buildInsertQuery(fullTableName, fieldNames, newVals);
                  }
                  stmts.push(sql);
              });
              console.log(stmts);
              $.each(stmts, function (index, sql) {
                  executeSQL(sql, function (res) {
                      // do nothing
                      return;
                  }, function (err) {
                      displayErrorMessage('Error in saving data.', err.message);
                      return;
                  });
              });
              unsavedData = [];
              updateTableData(fullTableName);
          });
      });

      // Returns the fields that are in the view including the formulas for computed columns
      // Returned as a dictionary of { fieldName: true }
      var getViewFields = function (viewName, callback) {
          executeSQL(buildGetViewDefQuery(viewName), function (res) {
              var sql = res.tuples[0].cells[0];
              sql = sql.slice(sql.indexOf('SELECT') + 7, sql.indexOf('FROM'));
              var fields = sql.split(',');
              var fields_set = {};
              $.each(fields, function (index, element) {
                  if (!fields_set[element.trim()]) {
                      fields_set[element.trim()] = true;
                  }
              });
              callback(fields_set);
          }, function (err) {
              displayErrorMessage('Could not retrieve columns in table.', err.message);
              return;
          });
          
      }

      // Sets the type of cell to reflect the type in DataHub
      // Make computed columns and p_key readOnly
      var refreshCellMeta = function (tableName) {
          var hot = $('#results').handsontable('getInstance');
          getColumnNames(tableName, function (realCols) {
              $.each(hot.getSettings().colHeaders, function (index, colData) {
                  var hasType = (realCols.indexOf(colData) > -1) ? true : false;
                  if (hasType) {
                      var dataType = getDataTypeForCol(colData);
                      var colDataType = { type: 'text' };
                      if (numberTypes.indexOf(dataType) > -1) {
                          // allowInvalid: false
                          colDataType = { type: 'numeric', format: '0,0[.]00' };
                      } else if (dataType === 'date') {
                          colDataType = { type: 'date', dateFormat: 'MM/DD/YYYY', correctFormat: true};
                      }
                  }
                  // run through all cells in col
                  for (var i = 0; i < hot.countRows(); i++) {
                      if (hasType) { 
                          $.each(Object.keys(colDataType), function (data_type_key_index, dataType) {
                              var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[i][0] : i;
                              hot.setCellMeta(cellRow, index, dataType, colDataType[dataType]);
                          });
                      }
                      if (colData === 'p_key' || !hasType) {
                          var cellRow = hot.sortIndex.length > 0 ? hot.sortIndex[i][0] : i;
                          hot.setCellMeta(cellRow, index, 'format', '0,0[.]00');
                          hot.setCellMeta(cellRow, index, 'type', 'numeric');
                          hot.setCellMeta(cellRow, index, 'readOnly', true);
                      } 
                  }
              });
              hot.render();
          });
      }

      // Adds a computed column to the view
      var addColToView = function (viewName, colExpr, colName) {
          getViewFields(viewName, function (fields_set) {
              tName = viewName.slice(viewName.lastIndexOf('.') + 1, viewName.indexOf('_view'));
              delete fields_set[tName + '.' + colName];
              fields_set['(' + colExpr + ') as ' + colName] = true;

              replaceView(viewName, fields_set);
          });
      }

      // Removes a column (computed or not) from the view
      var removeColFromView = function (viewName, colName) {
          getViewFields(viewName, function (fields_set) {
              var fieldToRemove = '';
              $.each(Object.keys(fields_set), function (index, key) {
                  if (key.substr(key.indexOf('AS') + 3) === colName) {
                      fieldToRemove = key;
                  }
              });
              delete fields_set[fieldToRemove];
              replaceView(viewName, fields_set);
          });
      }

      // Takes the current view and adds any columns present in the table to the view
      var refreshView = function (viewName) {
          var tName = viewName.slice(viewName.lastIndexOf('.') + 1, viewName.indexOf('_view'));
          getViewFields(viewName, function (fields_set) {
              getColumnNames(viewName.slice(0, viewName.indexOf('_view')), function (fieldNames) {
                  $.each(fieldNames, function (index, element) {
                      if (fields_set[element] === undefined) {
                          fields_set[tName + '.' + element] = true;
                      }
                  });
                  replaceView(viewName, fields_set);
              });
          });
      }

      // Drops the old view and creates a new one with the list of fields which are the keys in fields_set
      var replaceView = function (viewName, fields_set) {
          var new_cols = Object.keys(fields_set);
          // first drop existing view
          executeSQL(buildDropViewQuery(viewName, true), function (res) {
              // now create with new query
              executeSQL(buildCreateViewQuery(viewName, buildSelectQuery(viewName.slice(0, viewName.indexOf('_view')), new_cols)), function (res) {
                  updateTableData(viewName.slice(0, viewName.indexOf('_view')));
              }, function (err) {
                  displayErrorMessage('Could not create a new view.', err.message);
                  return;
              });
          }, function (err) {
              displayErrorMessage('Could not replace current view.', err.message);
              return;
          });
      }

      // Returns the index of the primary key column
      var getPKColNum = function (hot) {
          return getColNum(hot, 'p_key');
      }

      // Returns the index of the column with colName
      var getColNum = function (hot, colName) {
          for (var i = 0; i < hot.getSettings().colHeaders.length; i++) {
              if (hot.getColHeader(i) === colName) {
                  return i;
              }
          }
          return -1;
      }


      // prepare the add col modal
      $('#colTypes').select2({data: dataTypes });

      // Retrieve all data and populate the UI
      updateRepo(repoName);
  };
});

// Retreives information about the current repository and updates the table data 
// to show the current table
var updateRepo = function(newRepoName, tableToShow) {
    repoName = newRepoName;
    var tables = client.list_tables(con, repoName);
    var i = 0;
    while (tableToShow == null) {
        tableToShow = accountName + "." + repoName + "." + tables.tuples[i].cells[0];
        if (tableToShow.indexOf('_view') > -1) { tableToShow = null; }
        i++;
    }
    fullTableName = tableToShow;
    updateTableData(tableToShow);
    updateTableMenu(tableToShow.substr(accountName.length+1), tables);
    updateRepositoryMenu(repoName, repos);
}

// Updates the given table in the given repository
var updateCurrentTable = function(repoName, tableName) {
    // var tables = client.list_tables(con, repoName);
    var tables = datahub_utils.listTables()
    fullTableName = accountName + "." + repoName + "." +tableName;
    updateTableData(accountName + "." + repoName + "."+ tableName);
    updateTableMenu(repoName + "." + tableName, tables);
    updateRepositoryMenu(repoName, repos);
}

// Retrieves the data from DataHub, builds the data arrays
// Adds a primary key column if one does not exist
var updateTableData = function(tableName) {
    var shortTableName = tableName.slice(tableName.lastIndexOf('.') + 1);
    executeSQLQuietFail(buildCreateViewQuery(tableName + '_view', buildSelectQuery(tableName, ['*'])), function () {
        getColumnNames(tableName, function (colNames) {
            var buildData = function () {
                executeSQL(buildSelectQuery(tableName + '_view', ['*']), function (res) {
                    var data = res.tuples.map(function (tuple) { return tuple.cells; });
                    var hot = $('#results').handsontable('getInstance');
                    $('#results').data('handsontable').updateSettings({
                        data: data, 
                        colHeaders: res.field_names,
                    });
                    
                }, function (err) {
                    displayErrorMessage('Could not retrieve data from ' + tableName, err.message);
                    return;
                });
            }
            // decide if we need to create a p_key
            if (colNames.indexOf('p_key') === -1) {
                // Add p_key field
                    executeSQL(buildAddColumnQuery(tableName, 'p_key', 'SERIAL'), function (res) {
                        buildData();
                    }, function (err) {
                        displayErrorMessage('Could not add a primary key column.', err.message);
                        return;
                    });
            } else {
                buildData();
            }
        });        
    });
    
    unsavedData = [];
}

// Updates the menu of available tables
var updateTableMenu = function(currentTableName, tables) {
    $(".table-name").text(currentTableName);
    var shortTableName = currentTableName.substr(currentTableName.indexOf(".")+1);
    var table_names = tables.tuples.map(function (tuple) { return tuple.cells[0]; }).reverse();
    $(".table-link").remove();
    table_names.forEach(function (name) { 
        if (name.indexOf('_view') === -1) {
            var midName = repoName + "." + name;
            var tableLink = $("<li class='table-link'><a href='#'>"+midName+"</a></li>");
            tableLink.find("a").click(function() {
                //$('#results').handsontable('getInstance').runHooks('persistentStateReset');
                fullTableName = accountName + "." + midName;
                updateTableData(fullTableName);
                updateTableMenu(midName, tables); 
            });
            $(".tables-menu").prepend(tableLink);
        }
    });
    chart_client.setTableInfo(repoName, shortTableName);
}

// Updates the menu of available tables in the current repository 
var updateRepositoryMenu = function(currentRepoName, repos) {
    repoNames = repos.tuples.map(function (tuple) { return tuple.cells[0]; });
    $(".repo-link").remove();
    repoNames.forEach(function (name) {
        var repoLink = $("<li class='repo-link'><a href='#'>"+name+"</a></li>");
        repoLink.find("a").click(function() {updateRepo(name); });
        $(".tables-menu").append(repoLink);
        if (name == currentRepoName) {
            repoLink.addClass("disabled");
        }
    });
}


