/**
 * datahub.thrift
 * IDL for DataHub Services
 *
 * @author: Anant Bhardwaj
 * @date: 10/09/2013
 *
 */

namespace py datahub

const double VERSION = 1.0

exception DHException {
  1: i32 errorCode,
  2: string message,
  3: string details
}

struct DHDatabase {
  1: string url
  2: string name 
}

struct DHConnectionParams {
  1: string user,
  2: string password,
  3: DHDatabase database
}

struct DHConnection {
  1: string id,
  2: string user,
  3: DHDatabase database
}

struct DHColumnSpec{
  1: list <string> column_names,
  2: list <string> column_types
}

struct DHCell {
  1: binary value
}

struct DHRow {
  1: i32 id,
  2: list <DHCell> cells,
  3: i32 version_number
}

struct DHTable {
  1: i32 id,
  2: DHColumnSpec column_spec,
  3: list <DHRow> tuples,
  4: i32 version_number  
}

struct DHQueryResult {
  1: bool status,
  2: i32 row_count,
  3: DHTable table,
}

service DataHub {
  double get_version()
  DHConnection connect(1:DHConnectionParams con_params)
      throws (1: DHException ex)
  DHConnection open_database(1:DHConnection con, 2:DHDatabase database)
      throws (1: DHException ex)
  DHQueryResult list_databases(1:DHConnection con)
      throws (1: DHException ex)
  DHQueryResult list_tables(1:DHConnection con) throws (1: DHException ex)
  DHQueryResult execute_sql(1:DHConnection con, 2: string query,
      3: list <string> query_params) throws (1: DHException ex)
}