Feature: Checking installation of Datahub
  Scenario: Index page shows up
      Given Datahub is installed
      When I open "/"
      Then I should be redirected to "/www/"
      And I should see "What is DataHub?"
