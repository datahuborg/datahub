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
  5: optional string repo_base
}

// connection info -- must be passed in every execute_sql call
struct Connection {
  1: optional string client_id,
  2: optional string seq_id,
  3: optional string user,
  4: optional string repo_base,
  5: optional i64 cursor
}

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

enum TablePrivilegeType {
  NONE,
  SELECT,
  INSERT,
  UPDATE,
  DELETE,
  ALL
}

enum RepoPrivilegeType {
  NONE,
  LIST,  // allows listing of all the objects within a repo
  CREATE,  // allows creation of new object within a repo
  ALL
}

const list<TablePrivilegeType> DEFAULT_PRIVILEGES_TABLE = [
    TablePrivilegeType.SELECT,
    TablePrivilegeType.INSERT,
    TablePrivilegeType.UPDATE,
    TablePrivilegeType.DELETE]

struct AddRepoPrivilege {
  1: optional string repo_name,
  2: optional list<RepoPrivilegeType> privileges = [RepoPrivilegeType.CREATE]
}

struct AddTablePrivilege {
  1: optional list <TablePrivilegeType> privileges = DEFAULT_PRIVILEGES_TABLE,
  2: optional list <string> tables = ['ALL']
}

// privileges assigned while adding a collaborator
struct AddPrivilege {
  1: optional AddRepoPrivilege repo_privilege,
  2: optional AddTablePrivilege table_privilege,
  3: optional list <TablePrivilegeType>
      new_table_default_privileges = DEFAULT_PRIVILEGES_TABLE
}

struct RemoveRepoPrivilege {
  1: optional string repo_name,
  2: optional list<RepoPrivilegeType> privileges = [RepoPrivilegeType.ALL]
}

struct RemoveTablePrivilege {
  1: optional list <TablePrivilegeType> privileges = TablePrivilegeType.ALL,
  2: optional list <string> tables = ['ALL']
}

// privileges removed while removing a collaborator
struct RemovePrivilege {
  1: optional RemoveRepoPrivilege repo_privilege,
  2: optional RemoveTablePrivilege table_privilege
}

// Error in DB Operation
exception DBException {
  1: optional i32 error_code,
  2: optional string message,
  3: optional string details
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
      2: string username,
      3: AddPrivilege privilege) throws (1: DBException ex)

  ResultSet remove_collaborator (
      1: Connection con,
      2: string username,
      3: RemovePrivilege privilege) throws (1: DBException ex)

  ResultSet get_schema (
      1: Connection con, 2: string table_name) throws (1: DBException ex)

  ResultSet execute_sql (
      1: Connection con,
      2: string query,
      3: list <binary> query_params) throws (1: DBException ex)

  bool close_connection (1: Connection con) throws (1: DBException ex)
}
