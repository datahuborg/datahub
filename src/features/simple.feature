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