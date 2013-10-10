namespace py datahub

const double VERSION = 1.0

service DataHub {
  double get_version()

  bool create_database(1: string db_name)
  bool drop_database(1: string db_name)
  string show_databases()
  string show_tables(1: string db_name)

  string execute_sql(1: string db_name, 2: string query, 3: list<string> params, 4: bool commit)
}