/**
* Logic for constructing a PostgreSQL CREATE POLICY command from a
* DataQ.policy object.
*/
(function() {
  // If the global DataQ object does not exist, create it.
  window.DataQ = window.DataQ || {};

  /**
   * Take a DataQ.Policy object and generate a CREATE POLICY string from it.
   * A CREATE POLICY command looks like:
   *
   * CREATE POLICY name ON table_name
   *    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
   *    [ TO { role_name | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
   *    [ USING ( using_expression ) ]
   *    [ WITH CHECK ( check_expression ) ]
   *
   * see https://www.postgresql.org/docs/9.5/static/sql-createpolicy.html
   *
   * @param policy - The DataQ.policy object.
   * @return A String representing the CREATE POLICY command.
   */
  window.DataQ.build_policy = function(policy) {

    // Name of policy to be created.
    var policy_name = policy.name();

    // Name of table to which the policy applies.
    var table_name = policy.repo() + "." + policy.table_name();

    // Command to which the policy applies.
    var command = policy.command();

    // List of roles to which the policy applies.
    var role_list = policy.roles();

    // List of users to which the policy applies.
    // Each element must be one of { PUBLIC | CURRENT_USER | SESSION_USER }
    var user_list = policy.users();

    // SQL conditional expression to control row visibility.
    // Rows for which the expression returns true will be visible.
    var using_expr = policy.using_expression();

    // SQL conditional expression to control INSERT and UPDATE privileges.
    // Only rows for which the expression evaluates to true will be allowed.
    var check_expr = policy.check_expression();

    /* Build policy string */
    var policy_string = "CREATE POLICY " + policy_name;

    // ON clause
    policy_string += " ON " + table_name;

    // FOR clause
    policy_string += " FOR " + command;

    // TO clause
    policy_string += " TO " + role_list.join(", ");
    policy_string += ", " + user_list.join(", ");

    // USING clause
    policy_string += " USING " + using_expr;

    // WITH CHECK clause
    if (command !== "SELECT") {
      // A SELECT policy cannot have a WITH CHECK expression, as it only applies
      // in cases where records are being retrieved from the relation.
      policy_string += " WITH CHECK " + check_expr;
    }

    // Remove leading and trailing spaces and then append semicolon.
    policy_string.trim();
    policy_string += ";";

    return policy_string;

  };
})();
