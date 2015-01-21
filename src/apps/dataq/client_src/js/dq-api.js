/**
 * Helper for accessing DataQ API.
 */
(function() {
  // Create the global DataQ object if it doesn't exist.
  window.DataQ = window.DataQ || {};

  DataQ.API = {};

  // See dataq/views.py for description of result.
  DataQ.API.get_repos = function(callback) {
    $.get("/apps/dataq/api/", callback);
  };

  // See dataq/views.py for description of result.
  DataQ.API.get_tables = function(repo, callback) {
    $.get("/apps/dataq/api/" + repo + "/", callback);
  };

  // See dataq/views.py for description of result.
  DataQ.API.get_schema = function(repo, table, callback) {
    $.get("/apps/dataq/api/" + repo + "/" + table + "/", callback);
  };
})();
