/**
 * datahub.thrift
 * IDL for DataHub Services
 *
 * @author: Anant Bhardwaj
 * @date: 10/09/2013
 *
 */

namespace cpp datahub
namespace java datahub
namespace php datahub
namespace perl datahub
namespace py datahub
namespace rb datahub

/* DataHub constants */

// version info
const double VERSION = 1.0


/* Database Connection */

// connection parameters
struct ConnectionParams {
  1: optional string client_id,
  2: optional string seq_id,
  3: optional string user,
  4: optional string password,
  5: optional string repo_base,
  6: optional string repo
}

// connection info -- must be passed in every execute_sql call
struct Connection {
  1: optional string client_id,
  2: optional string seq_id,
  3: optional string user,
  4: optional string repo_base,
  5: optional string repo,
  6: optional i64 cursor
}


/* ResultSet */

// a tuple
struct Tuple {
  1: optional list <binary> cells
}

// a result set (list of tuples)
struct ResultSet {
  1: required bool status,
  2: optional Connection con,
  3: optional i64 num_tuples,
  4: optional i64 num_more_tuples,
  5: optional list <Tuple> tuples,
  6: optional list <string> field_names,
  7: optional list <string> field_types
}


/* DataHub Exceptions */

// generic exception
exception DBException {
  1: optional i32 error_code,
  2: optional string message,
  3: optional string details
}


/* DataHub service APIs */

service DataHub {
  double get_version()

  Connection open_connection (1: ConnectionParams con_params)
      throws (1: DBException ex)

  ResultSet create_repo (1: Connection con, 2: string repo_name)
      throws (1: DBException ex)

  ResultSet list_repos(1: Connection con)
      throws (1: DBException ex)

  ResultSet delete_repo (
      1: Connection con, 2: string repo_name, 3: bool force_if_non_empty)
      throws (1: DBException ex)

  ResultSet list_tables (1: Connection con, 2: string repo_name)
      throws (1: DBException ex)

  ResultSet print_schema (1: Connection con, 2: string table_name)
      throws (1: DBException ex)

  ResultSet execute_sql (
      1: Connection con, 2: string query, 3: list <binary> query_params)
      throws (1: DBException ex)

  bool close_connection (1: Connection con)
      throws (1: DBException ex)
}
