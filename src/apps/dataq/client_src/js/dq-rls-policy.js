/**
* The object for building a row-level security policy.
*/
(function() {
  // If the DataQ object doesn't exist, create it.
  window.DataQ = window.DataQ || {};

  DataQ.Policy = function() {

    // Create the object and initialize its contents.
    var that = {};
    that._repo_name = null;
    that._name = null;
    that._table = null;
    that._command = null;
    that._roles = [];
    that._using_expr = null;
    that._check_expr = null;

    /**
     * Get or set the repo name.
     *
     * @param repo_name - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The name of the repo.
     */
    that.repo = function(repo_name) {
      if (repo_name !== undefined) {
        that._repo_name = repo_name;
      }
      return that._repo_name;
    };

    /**
     * Get or set the name of the policy.
     *
     * @param policy_name - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The name of the policy.
     */
    that.name = function(policy_name) {
      if (policy_name !== undefined) {
        that._name = policy_name;
      }
      return that._name;
    };

    /**
     * Get or set the name of the table to which this policy will apply.
     *
     * @param table_name - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The name of the table.
     */
    that.table = function(table_name) {
      if (table_name !== undefined) {
        that._table = table_name;
      }
      return that._table;
    };

    /**
     * Get or set the command { ALL | SELECT | INSERT| UPDATE | DELETE } to which
     * this policy will apply.
     *
     * @param cmd - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The name of the command.
     */
    that.command = function(cmd) {
      if (cmd !== undefined) {
        that._command = cmd;
      }
      return that._command;
    };

    /**
     * Get or set the Roles to which this policy will apply.
     *
     * @param role_list - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The list of Roles.
     */
    that.roles = function(role_list) {
      if (role_list !== undefined) {
        if (!(role_list instanceof Array)) {
          role_list = [role_list]
        }
        that._roles = role_list;
      }
      return that._roles;
    };

    /**
     * Get or set the policy's using_expression.
     *
     * @param expr - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The full using_expression.
     */
    that.using_expression = function(expr) {
      if (expr !== undefined) {
        that._using_expr = expr;
      }
      return that._using_expr;
    };

    /**
     * Get or set the policy's check_expression.
     *
     * @param expr - If this argument is omitted (or undefined), this function acts as a
     *                    getter. Otherwise, it acts as a setter, setting the repo name.
     *
     * @return The full check_expression.
     */
    that.check_expression = function(expr) {
      if (expr !== undefined) {
        that._check_expr = expr;
      }
      return that._check_expr;
    };

    return that;

  };
})();
