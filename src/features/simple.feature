Feature: Checking installation of DataHub
  Scenario: Index page shows up
    Given DataHub is installed
    When I open "/"
    Then I should be redirected to "/www/"
    And I should see "What is DataHub?"

  Scenario: Login page shows up
    Given DataHub is installed
    When I open "/account/login"
    Then I should see "Returning User -- Sign in"

  Scenario: Registration page shows up
    Given DataHub is installed
    When I open "/account/register"
    Then I should see "Create a new account"

  # Behave isn't currently playing nicely with static files
  # ARC 2015-06-24
  
  # Scenario: Sphinx Docs show up
  #   Given DataHub is installed
  #   When I open "/static/docs/html/index.html"
  #   Then I should see "Table Of Contents"