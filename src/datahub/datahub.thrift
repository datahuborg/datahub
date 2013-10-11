namespace py datahub

const double VERSION = 1.0

exception DBException {
  1: i32 errorCode,
  2: string message,
  3: string details
}

struct DHConnection {
  1: string database,
  2: string user
}

struct QueryResult {
  1: bool status,
  2: i32 num_rows_affected,
  3: list <string> column_types,
  4: list <string> column_names,
  5: list <list <string>> tuples,
}

service DataHub {
  double get_version()

  QueryResult list_databases(1:DHConnection con) throws (1: DBException ex)

  QueryResult list_tables(1:DHConnection con) throws (1: DBException ex)

  QueryResult execute_sql(1:DHConnection con, 2: string query,  3: list <string> params) throws (1: DBException ex)
}