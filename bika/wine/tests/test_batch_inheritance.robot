*** Settings ***

Library          Selenium2Library  timeout=10  implicit_wait=0.2
Library          String
Resource         keywords.txt
Variables        plone/app/testing/interfaces.py
Suite Setup      Start browser
# Suite Teardown   Close All Browsers

*** Variables ***

${SELENIUM_SPEED}  0
${PLONEURL}        http://localhost:55001/plone

*** Test Cases ***

Test AR new changed and removed fields
    Log in         test_labmanager  test_labmanager
    ## Add batch
    go to                       ${PLONEURL}/batches
    Click Link                  Add
    wait until page contains    Add Group
    Input Text                  title           First Batch
    select from dropdown        Client          Happy
    Input Text                  description     This batch will contain five very simple ARs.
    Input Text                  WorksOrderID    woid1
    Input Text                  LabelAlcohol    15%
    SelectDate                  BatchDate       1
    Click Button                Save
    ## Add 5 Requests in Batch
    go to                       ${PLONEURL}/batches/B-001/analysisrequests
    select from list            css=select.col_count         5
    click link                  Add new
    wait until page contains    Request new analyses
    Select from dropdown        ar_0_Contact    Rita
    Click element               css=.ContactCopyButton
    SelectDate                  ar_0_SamplingDate            1
    Click element               css=.SamplingDateCopyButton
    Select from dropdown        ar_0_SampleType    Water
    Click element               css=.SampleTypeCopyButton
    Click element               css=#cat_lab_Metals
    Select checkbox             xpath=//input[@title='Calcium'][1]
    Click element               xpath=//img[@name='Calcium']
    Set Selenium Timeout        30
    Click Button                Save
    Wait until page contains    created
    Set Selenium Timeout        10

    ## Add second batch
    Go to                       ${PLONEURL}/batches
    Click Link                  Add
    Input Text                  title           second Batch
    select from dropdown        Client          Happy
    Input Text                  description     Inherit, delete, rinse, repeat
    Input Text                  WorksOrderID    woid2
    Input Text                  LabelAlcohol    25%
    SelectDate                  BatchDate       1
    Click Button                Save

    go to                       ${PLONEURL}/batches/B-002/base_edit
    click element               InheritedObjectsUI_more
    click element               InheritedObjectsUI_more
    click element               InheritedObjectsUI_more
    click element               InheritedObjectsUI_more
    select from dropdown        InheritedObjectsUI-Title-0    0001
    select from dropdown        InheritedObjectsUI-Title-1    0002
    select from dropdown        InheritedObjectsUI-Title-2    0003
    select from dropdown        InheritedObjectsUI-Title-3    0004
    select from dropdown        InheritedObjectsUI-Title-4    0005
    Click button                Save

    go to                       ${PLONEURL}/batches/B-002/base_edit
    Click element               delete-row-0
    Click button                Save
    go to                       ${PLONEURL}/batches/B-002/base_edit
    page should not contain element    delete-row-5


*** Keywords ***

Start browser
    Open browser         http://localhost:55001/plone/
    Set selenium speed   ${SELENIUM_SPEED}
