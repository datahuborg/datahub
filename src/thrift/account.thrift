/**
 * account.thrift
 * IDL for DataHub Acoount Services
 *
 * @author: Anant Bhardwaj
 * @date: 10/09/2013
 *
 */


namespace cocoa datahub_account
namespace cpp datahub.account
namespace go datahub.account
namespace java datahub.account
namespace py datahub.account
namespace rb datahub.account


// Error in Account Creation
exception AccountException {
  1: optional i32 error_code,
  2: optional string message,
  3: optional string details
}

// service APIs
service AccountService {
  double get_version()
  
  bool create_account (
      1: string username,
      2: string email,
      3: string password,
      4: string repo_name,
      5: string app_id,
      6: string app_token) throws (1: AccountException ex)

  bool remove_account (
      1: string username,
      2: string app_id,
      3: string app_token) throws (1: AccountException ex)
}
