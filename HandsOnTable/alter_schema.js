$(document).ready(function(){
	$('#schemaModal').find("#submitAlts").click(function() {
		schemaAlts = [];
		// find what changed
		var res = client.get_schema(con, fullTableName);
		res.tuples.forEach(function (tuple, index) {
			if (tuple.cells[1] !== $('#dropdown' + index).text()) {
				schemaAlts.push({ col: tuple.cells[0], newType: $('#dropdown' + index).text() });
			}
		});
		schemaAlts.forEach(function (schemaAlt) {
			viewQuery = buildGetViewDefQuery(fullTableName + '_view');
			console.log(schemaAlt);
			var colName = schemaAlt['col'];
			executeSQL('begin;', function (res) {
				queryList = [buildAddColumnQuery(fullTableName, 'temp', schemaAlt.newType)];
				queryList.push(buildUpdateQuery(fullTableName, {'temp' : 'cast(' + schemaAlt.col + ' as ' + schemaAlt.newType + ')'}));
				queryList.push(buildDropColumnQuery(fullTableName, schemaAlt.col, true));
				queryList.push(buildAddColumnQuery(fullTableName, schemaAlt.col, schemaAlt.newType));
				changesObj = {};
				changesObj[schemaAlt.col] = 'temp';
				queryList.push(buildUpdateQuery(fullTableName, changesObj));
				queryList.push(buildDropColumnQuery(fullTableName, 'temp'));
				queryList.push(buildCreateViewQuery(fullTableName + '_view', viewQuery));
				executeSQL(queryList.join('; '), function (res) {
					// commit the transaction
					executeSQL('commit;', function (res) {
						// TODO (jennya)
						return;
					}, function (err) {
						// TODO (jennya)
						return;
					});
				}, function (err) {
					// abort the transaction
					console.log('aborting...');
					executeSQL('rollback;', function (res) {
						// TODO (jennya)
						return;
					}, function (err) {
						// TODO (jennya)
						return;
					});
				});
			}, function (err) {
				// TODO (jennya)
				return;
			});
		});
	});
	$(document).on('click', '#alterSchemaButton', function() {
		$('#schemaModal').find('.modal-title').html("Alter the Schema");
		$('#schemaModal').find('.modal-body').html('<table class="table table-striped" id="schemaList"></table>');

		var res = client.get_schema(con, fullTableName);
		res.tuples.forEach(function (tuple, index) {
			// console.log(tuple);
			$('#schemaModal').find('#schemaList').append(
				'<tr>' + 
					'<td>' + 
						tuple.cells[0] + 
					'</td>' + 
					'<td>' + 
						'<div class="btn-group"> <a id="dropdown' + index + '" class="btn btn-default dropdown-toggle btn-select" data-toggle="dropdown" href="#">' + tuple.cells[1] + '<span class="caret"></span></a>' + 
				            '<ul class="dropdown-menu">' + 
				                '<li><a href="#">bigint</a></li>' + 
				                '<li><a href="#">bit</a></li>' + 
				                '<li><a href="#">decimal</a></li>' + 
				                '<li><a href="#">int</a></li>' + 
				                '<li><a href="#">money</a></li>' + 
				                '<li><a href="#">numeric</a></li>' + 
				                '<li><a href="#">smallint</a></li>' + 
				                '<li><a href="#">smallmoney</a></li>' + 
				                '<li><a href="#">tinyint</a></li>' + 
				                '<li class="divider"></li>' + 
				                '<li><a href="#">float</a></li>' + 
				                '<li><a href="#">real</a></li>' + 
				                '<li class="divider"></li>' + 
				                '<li><a href="#">date</a></li>' + 
				                '<li><a href="#">datetime2</a></li>' + 
				                '<li><a href="#">datetime</a></li>' + 
				                '<li><a href="#">datetimeoffset</a></li>' + 
				                '<li><a href="#">smalldatetime</a></li>' + 
				                '<li><a href="#">time</a></li>' + 
				                '<li class="divider"></li>' + 
				                '<li><a href="#">char</a></li>' + 
				                '<li><a href="#">text</a></li>' + 
				                '<li><a href="#">varchar</a></li>' + 
				                '<li class="divider"></li>' + 
				                '<li><a href="#">nchar</a></li>' + 
				                '<li><a href="#">ntext</a></li>' + 
				                '<li><a href="#">nvarchar</a></li>' + 
				                '<li class="divider"></li>' + 
				                '<li><a href="#">binary</a></li>' + 
				                '<li><a href="#">image</a></li>' + 
				                '<li><a href="#">varbinary</a></li>' + 
				                '<li class="divider"></li>' + 
				                '<li><a href="#">cursor</a></li>' + 
				                '<li><a href="#">hierarchyid</a></li>' + 
				                '<li><a href="#">sql_variant</a></li>' + 
				                '<li><a href="#">table</a></li>' + 
				                '<li><a href="#">timestamp</a></li>' + 
				                '<li><a href="#">uniqueidentifier</a></li>' + 
				                '<li><a href="#">xml</a></li>' + 
				            '</ul>' + 
				        '</div>' + 
					'</td>' + 
				'</tr>');
		});
	});
 	$(document).on('click', '.dropdown-menu li a', function(){
	  var selText = $(this).text();
	  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+'<span class="caret"></span>');
	});
});