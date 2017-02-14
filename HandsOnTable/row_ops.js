$(document).ready(function(){
	$('#columnModal').find(".go_button").click(function() {
		parseExpression($('#expressionText').val(), $('#columnName').val());
	});
	$(document).on('click', '#addColumnButton', function() {
		$('#columnModal').find('.modal-title').html("Add a New Column");
		$('#columnModal').find('#expressionText').val('');
		$('#columnModal').find('#columnName').val('');
	});
 
});

// Returns the SQL query associated with the expression
function parseExpression(text, colName) {
	console.log(text + ' ' + colName);
	if (colName === '') {
		colName = 'aggCol';
	}
	var expr = Parser.parse(text);
	sql_commands = expr.toSQL(false, colName);
	console.log(sql_commands);
	var res;
	sql_commands.forEach(function (sql) {
		res = client.execute_sql(con, sql);
	});

	// close modal and update table
	updateTableData(fullTableName);
};