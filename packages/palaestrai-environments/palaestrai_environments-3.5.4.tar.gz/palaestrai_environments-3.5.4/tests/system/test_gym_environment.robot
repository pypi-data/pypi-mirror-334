*** Settings ***
Documentation   Test handling of single line execution
...
...             This calls the single line execution with the dummy experiment on the gym environment.
...             The test then monitors that the execution returns 0.

Library         Process
Library         OperatingSystem
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt

*** Test Cases ***
Call palaestrai experiment-start with the gym_eyperiment.yml.
    ${result} =                     Run Process         palaestrai      experiment-start     ${CURDIR}${/}..${/}fixtures${/}gym_experiment.yml  stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   0
