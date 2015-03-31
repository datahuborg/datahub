module.exports = function(query, hidden_cols) {
  try {
    var lower_case_query = query.toLowerCase();
    var select_end = lower_case_query.indexOf("select") + "select".length;
    var from_start = lower_case_query.indexOf("from");
    var select_string = query.substring(select_end, from_start);
    var select_arr = select_string.trim().split(",");

    var new_select_arr = [];
    var colname;
    for (var i = 0; i < select_arr.length; i++) {
      colname = select_arr[i].trim();
      if (hidden_cols[colname] === true) {
        continue;
      }
      new_select_arr.push(colname);
    }

    var final_query = query.substring(0, select_end) + " " + new_select_arr.join(", ") + " " + query.substring(from_start);
    return final_query;
  } catch (ex) {
    return query;
  }
};
