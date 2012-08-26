Feature: Retrieve a list of Gists
    In order to manage my of Gists
    As a fucking good programmer
    I want to retrieve a my list of Gists

    Scenario: Get a list of Gists without informing user and password
        Given None user
        Given None password
        When Request list of Gists
        Then The Result is False

