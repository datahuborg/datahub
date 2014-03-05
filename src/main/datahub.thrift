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
const double VERSION = 0.1


/* DataHub Table Schema */
enum DHType {
  Boolean,
  Integer,
  Double,
  Text,
  Binary,
  Date,
  DateTime,
  TimeStamp
}

struct DHIndex {
  1: optional bool primary,
  2: optional bool unique,
  3: optional bool btree_index,
  4: optional bool fulltext_index
}

union DHOrder {
  1: optional bool ascending,
  2: optional bool descending
}

union DHDefault {
  1: optional binary value,
  2: optional bool set_null,
  3: optional bool set_current_timestamp
}

struct DHForeignKey {
  1: optional i32 id,
  2: optional i32 version_number,
  3: optional string table_name,
  4: optional string field_name, 
}

struct DHField {
  1: optional i32 id,
  2: optional i32 version_number,
  3: optional string name,
  4: optional DHType type,
  5: optional i32 length,
  6: optional DHDefault default_val,
  7: optional list <DHIndex> indexes,
  8: optional bool null_allowed,
  9: optional bool auto_increment,
  10: optional DHOrder order,
  11: optional DHForeignKey reference
}

struct DHSchema {
  1: optional i32 id,
  2: optional i32 version_number,
  3: optional string name,
  4: optional list <DHField> fields,
}


/* DataHub Table */
struct DHCell {
  1: optional binary value
}

struct DHRow {
  1: optional i32 id,
  2: optional i32 version_number,
  3: optional list <DHCell> cells,
}

struct DHTable {
  1: optional i32 id,
  2: optional i32 version_number,
  3: optional list <DHRow> rows
}

struct DHData {
  1: optional DHSchema schema,
  2: optional DHTable table, 
}


/* DataHub Query Result */
struct DHQueryResult {
  1: required bool status,
  2: optional i32 error_code,
  3: optional i32 row_count,
  4: optional DHData data,
}


/* DataHub Connection */
struct DHConnectionParams {
  1: optional string user,
  2: optional string password,
  3: optional string repo
}

struct DHConnection {
  1: optional string id,
  2: optional string user,
  3: optional string repo
}


/* DataHub Exceptions */
// Generic Exception
exception DHException {
  1: optional i32 errorCode,
  2: optional string message,
  3: optional string details
}


/* DataHub service APIs */
service DataHub {
  double get_version()

  DHConnection connect (1: DHConnectionParams con_params)
      throws (1: DHException ex)

  DHQueryResult create_repo (1: DHConnection con, 2: string repo) throws (
      1: DHException ex)

  DHQueryResult list_repos(1: DHConnection con)
      throws (1: DHException ex)

  DHQueryResult delete_repo (1: DHConnection con, 2: string repo,
      3: bool force) throws (1: DHException ex)

  DHQueryResult list_tables (1: DHConnection con, 2: string repo) throws (
      1: DHException ex)

  DHQueryResult desc_table (1: DHConnection con, 2: string table) throws (
      1: DHException ex)

  DHQueryResult execute_sql (1: DHConnection con, 2: string query,
      3: list <string> query_params) throws (1: DHException ex)
}
