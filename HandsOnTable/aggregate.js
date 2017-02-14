$(document).ready(function(){
	$('#aggregateModal').on('click', '.go_button', function () {
		executeAggregateQuery(generateQuery());
	});
	$('#aggregateButton').click (function() {
	    var aggregateModal = $('#aggregateModal');
	    aggregateModal.find(".go_button").show();
	    $("#openNewTableButton").hide();
	    aggregateModal.find(".modal-header").removeClass("aggregateHeaderTable");
		aggregateModal.find('.modal-title').html("Create aggregation");
		aggregateModal.find('.modal-body').html("");
		aggregateModal.find('.modal-body').append("<div id='aggregateSelectionDiv'><form class='form-horizontal'><fieldset id='aggregateFieldset'></fieldset></form></div>");
		$("#aggregateFieldset").append('<div class="aggregateSection"> </div>');
		addAggregateSection(0);
		addGroupBySection ();
	});
 
});

function addAggregateSection (rowNumber) {
    
	$(".addMoreButton").hide();
	inputsectionId = 'aggregateInputSection'+rowNumber;
	$(".aggregateSection").append('<div id="'+inputsectionId+'" class="aggregateInputSection well"><div>')
	var inputSectionText = '<div class="form-group">'+ 
		'<label class="control-label col-sm-3" for="aggregateType">Function</label>'+
  		'<div class="col-sm-8">'+
    		'<select id="aggregateType'+rowNumber+'" name="aggregateType" class="input-xlarge form-control">'+
    			'<option>None</option>'+
    			'<option>Count</option>'+
      			'<option>Sum</option>'+
      			'<option>Average</option>'+
      			'<option>Max</option>'+
      			'<option>Min</option>'+
    		'</select></div>';
    		if (rowNumber>0) {
    			inputSectionText+='<span id="deleteRow'+rowNumber+'" class="glyphicon glyphicon-remove" aria-hidden="true"></span>';
    		}
  		inputSectionText+='</div>';
	$("#"+inputsectionId).append(inputSectionText);
	$("#deleteRow"+rowNumber).click (function() {
		$('#aggregateInputSection'+(rowNumber-1)).remove();
		rowNumber-=1;
	})

		$("#"+inputsectionId).append('<div class="control-group form-group">'+ 
		'<label class="control-label col-sm-3" for="aggregateType">Column</label>'+
  		'<div class="col-sm-8">'+
    		'<select id="aggregateColumn'+rowNumber+'" name="aggregateType" class="input-xlarge form-control">'+
    		'</select>'+
  		'</div></div>');
	
	var columns = $("#results").handsontable("getColHeader");
	i=0;
	for (var i = 0; i < columns.length; i++) { 
		$("#aggregateColumn"+rowNumber).append('<option>'+columns[i]+'</option>');
	}

	rowNumber = rowNumber+1;

	$("#"+inputsectionId).append("<a class='col-xs-offset-2 addMoreButton' onclick='addAggregateSection("+rowNumber+")'>+Add more</a>");

}

function addGroupBySection () {
	$("#aggregateFieldset").append('<div class="container-fluid"> <div class="row well aggregateGroupBySection"></br></div></div>');
	$(".aggregateGroupBySection").append('<div class="form-group">'+ 
		'<label class="control-label col-sm-3" for="aggregateType">Group By</label>'+
  		'<div class="col-sm-8">'+
    		'<select id="groupByColumn" name="aggregateType" class="input-xlarge form-control">'+
    		'<option>None</option>'+
    		'</select>'+
  		'</div></div>');
	var columns = $("#results").handsontable("getColHeader");
	// console.log(columns);
	for (i = 0; i < columns.length; i++) { 
		$("#groupByColumn").append('<option>'+columns[i]+'</option>');
	}

}

function addAggregateOption (rowNumber) {
	$('#aggregateSelectionDiv').append("</br>"+generateAggregateSection(rowNumber));
}

function generateQuery () {
	numRows = $(".aggregateInputSection").length;
	var query = "SELECT ";
    if ($("#groupByColumn").val() != "None") {
        query += $("#groupByColumn").val() +", ";
    }
	for (i = 0; i < numRows; i++) { 
		var currentaggregateColumn = $("#aggregateColumn"+i).val();
		var currentaggregateType = $("#aggregateType"+i).val();
		if ($("#aggregateType"+i).val()=='None') {
			query+= $("#aggregateColumn"+i).val()+" ";
		} else {
			if ($("#aggregateType"+i).val()=='Sum') {
			query+= "sum(cast("+$("#aggregateColumn"+i).val()+" as float)) ";
		} else if ($("#aggregateType"+i).val()=='Average') {
			query+= "avg(cast("+$("#aggregateColumn"+i).val()+" as float)) ";
		} else {
			query+= $("#aggregateType"+i).val()+"("+$("#aggregateColumn"+i).val()+") ";
		}
		query += "as "+currentaggregateType+currentaggregateColumn+" ";
		}
		if(i<numRows-1) {
			query+=",";
		}
	}
	query+="from "+fullTableName;
	if ($("#groupByColumn").val() !="None") {
		query+=" group by "+$("#groupByColumn").val();
	} 
    $("#aggregateModal").find(".go_button").unbind("click");
    $("#aggregateModal").find(".go_button").hide(); //TODO close modal and switch to other context
	return query;
}

function executeAggregateQuery(query) {
	res = executeQuery(query)
    var aggregateModal = $("#aggregateModal");

	aggregateModal.find(".modal-body").html("<table id='aggregateResults'></table>");
	var data = res.tuples.map(function (tuple) { return tuple.cells; });
	var columnNames = res.field_names;
	$('#aggregateResults').handsontable({
		data: data,
		minSpareRows: 1,
		colHeaders: columnNames,
		contextMenu: true
	});
	aggregateModal.find(".modal-title").html('<div id="createTable"><button type="button" class="btn btn-default" id="save_button">Save as new Table</button></div>');
	$("#save_button").click (function () {
		aggregateModal.find(".modal-header").addClass("aggregateHeaderTable");
		$("#createTable").html('<div class="col-sm-8"><input class="form-control" id="newNameInput" placeholder="Type New Name Here"></div><button type="button" class="btn btn-default col-sm-3" id="save_button">Save</button>');
		$("#save_button").click(function() {
			aggregateModal.find(".modal-header").removeClass("aggregateHeaderTable");
			var newName = $("#newNameInput").val();
			newquery="CREATE TABLE "+accountName+"."+repoName+"."+newName+" AS ("+ query+")";
			executeQuery(newquery);
			aggregateModal.find(".modal-title").html("Table "+newName+' successfully created!');
			$("#openNewTableButton").html("Open "+newName);
			$("#openNewTableButton").show();
			$("#openNewTableButton").click(function () {
				updateCurrentTable(repoName,newName);
			});
            updateRepo(repoName, fullTableName);
		});
	});
}

// function executeQuery(query) {
//     transport = new Thrift.Transport("http://datahub.csail.mit.edu/service/json"),
// 	protocol = new Thrift.Protocol(transport),
// 	client = new DataHubClient(protocol),
// 	con_params = new ConnectionParams({'user': accountName, 'password': password}),
// 	con = client.open_connection(con_params),
// 	res = client.execute_sql(con, query);
// 	return res;
// }

