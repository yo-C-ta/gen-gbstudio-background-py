Feature: Compose a PNG image file with a CSV file

  Scenario Outline: Compose a PNG image file with a CSV file
    Given we have a "<grid>" file in CSV
    And we have a "<config>" file in JSON
    When we run the composer
    Then we get an output file in PNG like this "<image>"

  Examples: Inputs and output
    | grid             | config             | image                        | 
    | sample/field.csv | sample/config.json | sample/output/background.png |
