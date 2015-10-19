/**
 * rowsecurity.thrift
 * Row Level Security for Datahub
 *
 * @author: Kelly Zhang
 * @date: 2/21/2015
 *
 */

namespace cocoa datahub_rowsecurity
namespace cpp datahub.rowsecurity
namespace go datahub.rowsecurity
namespace java datahub.rowsecurity
namespace py datahub.rowsecurity
namespace rb datahub.rowsecurity

struct SecurityPolicy {
  1: required string table_name,
  2: required string command_name,
  3: optional list <string> predicates,
}

struct PolicySet {
  1: optional list <SecurityPolicy> policies,
}

exception DBException {
	1: optional i32 error_code,
	2: optional string message,
	3: optional string details,
}

exception QueryException {
  1: optional i32 error_code,
	2: optional string message,
	3: optional string details,
}

service RowSecurityService {
	
  bool create_security_policy (
    1: string user_name,
    2: SecurityPolicy policy) throws (1: DBException ex)

  bool update_security_policy (
    1: string user_name,
    2: SecurityPolicy policy) throws (1: DBException ex)

  SecurityPolicy view_security_policy ( 
    1: string user_name,
    2: string table_name,
    3: string command_name) throws (1: DBException ex)

  bool remove_recurity_policy ( 
    1: string user_name,
    2: SecurityPolicy policy) throws (1: DBException ex)

  PolicySet view_policy_set (
    1: string user_name)

  string filter_sql_query ( 
    1: string user_name,
    2: string sql_query) throws (1: QueryException ex)

}


