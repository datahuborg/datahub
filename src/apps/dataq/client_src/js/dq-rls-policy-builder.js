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
    var table_name = policy.repo() + "." + policy.table();

    // Command to which the policy applies.
    var command = policy.command();

    // List of roles to which the policy applies.
    var role_list = policy.roles();

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

    // USING clause
    if (command !== "INSERT") {
      policy_string += " USING " + using_expr;
    } else if (using_expr !== null) {
      var err_msg = "An INSERT policy cannot have a USING expression, as USING is"
                    + " used for reading existing records, not adding new ones.";
      alert(err_msg);
      return null;
    }

    // WITH CHECK clause
    if (command !== "SELECT" && command !== "DELETE") {
      // Neither a SELECT or DELETE policy can have a WITH CHECK expression,
      // as this expression is used for validating new records, not reading or
      // deleting existing ones.
      policy_string += " WITH CHECK " + check_expr;
    } else if (check_expr !== null) {
      var err_msg = "Neither a SELECT or DELETE policy can have a WITH CHECK expression"
                + ", as this expression is used for validating new records, not"
                + " reading or deleting existing ones.";
      alert(err_msg);
      return null;
    }

    // Remove leading and trailing spaces and then append semicolon.
    policy_string.trim();
    policy_string += ";";

    return policy_string;

  };
})();
