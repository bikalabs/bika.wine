*** Settings ***

Library                 Selenium2Library  timeout=10  implicit_wait=0.2
Resource                keywords.txt
Suite Setup             Start browser
Suite Teardown          Close All Browsers

*** Variables ***

${SELENIUM_SPEED}  0
${PLONEURL}        http://localhost:55001/plone

*** Test Cases ***

Test AR new changed and removed fields
    Log in                              test_labmanager         test_labmanager
    ## Add Batch
    Go to                               ${PLONEURL}/batches
    Click Link                          Add
    Input Text                          title                   First Batch
    Select from dropdown                Client                  Happy
    Input Text                          description             Nothing to see here...
    Input Text                          WorksOrderID            woid1
    Input Text                          LabelAlcohol            15%
    Click element                       BatchDate
    Click Link                          1
    Click Button                        Save
    ## Add Requests in Batch
    go to                               ${PLONEURL}/batches/B-001/analysisrequests
    click Link                          Add new
    ### Check that field defaults
    ### were filled correctly
    ${batch_name} =                     Get value               css=#ar_0_Batch
    Should be equal                     ${batch_name}           First Batch        Batch should be "First Batch" in this batch's context
    ### Add a new client
    Go to                               ${PLONEURL}/clients
    Click link                          Add
    Input Text                          Name                    Second Client
    Input Text                          ClientID                SecondClient
    Click Button                        Save
    Wait until page contains            Changes saved.
    Go to                               ${PLONEURL}/clients
    Click Link                          Second Client
    Click Link                          Contacts
    Click Link                          Add
    Input Text                          Firstname               Andrew
    Input Text                          Surname                 Dobbs
    Click Button                        Save
    ### Add Requests in Client
    Click Link                          Second Client
    Click Link                          Add
    ### Check that field defaults
    ### were filled correctly
    ${batch_name} =                     Get value               css=#ar_0_Batch
    Should be equal                     ${batch_name}           \               Batch should be empty in Client context
    ${client_name} =                    Get value               css=#ar_0_Client
    Should be equal                     ${client_name}          Second Client   Client should be "Second Client" in this client's context

Test SampleType fields
    Log in                              test_labmanager         test_labmanager

    Go to                               ${PLONEURL}/bika_setup/bika_sampletypes
    Click link                          Red Wine
    Click link                          Wine
    ### Set values
    select from dropdown                WineType                Red        1
    Input text                          Vintage                 a_vintage
    Input text                          Varietal                a_varietal
    select from dropdown                Region                  North      1
    Input Text                          LabelAlcohol            15%
    Select from dropdown                TransportConditions     between
    Select from dropdown                StorageConditions       sunlight
    Input text                          ShelfLifeType           shelflife_type
    Input text                          ShelfLife               3
    Click button                        Save
    Page should contain                 Changes saved
    ### Check values saved correctly
    Click link                          Wine
    ${value} =                          Get Value               WineType
    Should be equal                     ${value}                Red Wine
    ${value} =                          Get Value               Vintage
    Should be equal                     ${value}                a_vintage
    ${value} =                          Get Value               Varietal
    Should be equal                     ${value}                a_varietal
    ${value} =                          Get Value               Region
    Should be equal                     ${value}                North             # buglet: shows only 'Title', tho ui_item=Name.
    ${value} =                          Get Value               LabelAlcohol
    Should be equal                     ${value}                15.0
    Xpath Should Match X Times          //div[@class='reference_multi_item']//img[@class='deletebtn']    2

Test batch inherited ARs
    Log in                              test_labmanager         test_labmanager

    ## Add batch
    Go to                               ${PLONEURL}/batches
    Click Link                          Add
    Input Text                          title                   First Batch
    select from dropdown                Client                  Happy
    Input Text                          description             contains ARs.
    Input Text                          WorksOrderID            IWOID1
    Input Text                          LabelAlcohol            25%
    SelectDate                          BatchDate               1
    Click Button                        Save

    go to                               ${PLONEURL}/batches/B-001/analysisrequests
    select from list                    col_count           6
    click link                          Add new
    wait until page contains            Request new analyses
    Select from dropdown                ar_0_Contact            Rita
    Click element                       css=.ContactCopyButton
    SelectDate                          ar_0_SamplingDate       1
    Click element                       css=.SamplingDateCopyButton
    Select from dropdown                ar_0_SampleType         Water
    Click element                       css=.SampleTypeCopyButton
    Click element                       css=#cat_lab_Metals
    Select checkbox                     xpath=//input[@title='Calcium'][1]
    Click element                       xpath=//img[@name='Calcium']
    Set Selenium Timeout                30
    Click Button                        Save
    Wait until page contains            created
    Set Selenium Timeout                10

    ## Add second batch
    Go to                               ${PLONEURL}/batches
    Click Link                          Add
    Input Text                          title           Second Batch
    select from dropdown                Client          Happy
    Input Text                          description     Inherit, delete, rinse, repeat
    Input Text                          WorksOrderID    IWOID2
    Input Text                          LabelAlcohol    25%
    SelectDate                          BatchDate       1
    Click Button                        Save

    go to                               ${PLONEURL}/batches/B-002/base_edit
    click element                       InheritedObjectsUI_more
    click element                       InheritedObjectsUI_more
    click element                       InheritedObjectsUI_more
    click element                       InheritedObjectsUI_more
    select from dropdown                InheritedObjectsUI-Title-0    0001
    select from dropdown                InheritedObjectsUI-Title-1    0002
    select from dropdown                InheritedObjectsUI-Title-2    0003
    select from dropdown                InheritedObjectsUI-Title-3    0004
    select from dropdown                InheritedObjectsUI-Title-4    0005
    Click button                        Save

    go to                               ${PLONEURL}/batches/B-002/base_edit
    Click element                       delete-row-0
    Click button                        Save
    go to                               ${PLONEURL}/batches/B-002/base_edit
    page should not contain element     delete-row-5
    Click element                       delete-row-0
    Click element                       delete-row-1
    Click element                       delete-row-2
    Click element                       delete-row-3
    select from dropdown                InheritedObjectsUI-Title-4    IWOID1
    click button                        Save
    go to                               ${PLONEURL}/batches/B-002/batchbook


*** Keywords ***

Start browser
    Open browser         http://localhost:55001/plone/
    Set selenium speed   0
