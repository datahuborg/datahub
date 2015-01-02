/**
 * datahub.thrift
 * IDL for DataHub Core DB Services
 *
 * @author: Anant Bhardwaj
 * @date: 10/09/2013
 *
 */

include "shared/types.thrift"

namespace cocoa datahub
namespace cpp datahub
namespace go datahub
namespace java datahub
namespace py datahub
namespace rb datahub


/* DataHub Core */

// connection parameters
struct ConnectionParams {
  1: optional string client_id,
  2: optional string seq_id,
  3: optional string user,
  4: optional string password,
  5: optional string repo_base,
}

// connection info -- must be passed in every execute_sql call
struct Connection {
  1: optional string client_id,
  2: optional string seq_id,
  3: optional string user,
  4: optional string repo_base,
  5: optional i64 cursor,
}

// a tuple
struct Tuple {
  1: optional list <binary> cells,
}

// a result set (list of tuples)
struct ResultSet {
  1: required bool status,
  2: optional Connection con,
  3: optional i64 num_tuples,
  4: optional i64 num_more_tuples,
  5: optional list <Tuple> tuples,
  6: optional list <string> field_names,
  7: optional list <string> field_types,
}

enum CollaboratorType {
  USER,
  APP,
  ORGANIZATION,
}

struct Collaborator {
  1: optional CollaboratorType collaborator_type = CollaboratorType.USER,
  2: optional string name,
}

enum TableAccessPrivilege {
  SELECT = 0,
  INSERT = 1,
  UPDATE = 2,
  DELETE = 3,
}

enum RepoAccessPrivilege {
  LIST = 0,  // allows listing of all the objects within a repo
  CREATE = 1,  // allows creation of new objects within a repo
}

enum PrivilegeType {
  NONE = 0,
  PRIVILEGES_LIST = 1,
  ALL = 2,
}

struct RepoPrivilege {
  1: optional string repo_name,
  2: optional PrivilegeType privilege_type = PrivilegeType.ALL,
  3: optional list <RepoAccessPrivilege> privileges,
}

struct TablePrivilege {
  1: optional PrivilegeType privilege_type = PrivilegeType.ALL
  2: optional list <TableAccessPrivilege> privileges,
  3: optional bool apply_to_all_tables = true,
  4: optional bool default_for_future_tables = true,
  5: optional string table_name,
}

// privileges associated with a collaborator
struct Privilege {
  1: optional RepoPrivilege repo_privilege,
  2: optional TablePrivilege table_privilege,
}

// Error in DB Operation
exception DBException {
  1: optional i32 error_code,
  2: optional string message,
  3: optional string details,
}

// service APIs
service DataHub {
  double get_version()

  Connection open_connection (
      1: ConnectionParams con_params) throws (1: DBException ex)

  ResultSet create_repo (
      1: Connection con, 2: string repo_name) throws (1: DBException ex)

  ResultSet list_repos(1: Connection con) throws (1: DBException ex)

  ResultSet delete_repo (
      1: Connection con,
      2: string repo_name,
      3: bool force_if_non_empty) throws (1: DBException ex)

  ResultSet add_collaborator (
      1: Connection con,
      2: Collaborator collaborator,
      3: Privilege privilege) throws (1: DBException ex)

  ResultSet remove_collaborator (
      1: Connection con,
      2: Collaborator collaborator,
      3: Privilege privilege) throws (1: DBException ex)

  ResultSet get_schema (
      1: Connection con, 2: string table_name) throws (1: DBException ex)

  ResultSet execute_sql (
      1: Connection con,
      2: string query,
      3: list <binary> query_params) throws (1: DBException ex)

  bool close_connection (1: Connection con) throws (1: DBException ex)
}
