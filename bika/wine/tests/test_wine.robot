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
    sleep    2
    Log in                              test_labmanager         test_labmanager
    sleep    2
    ## Add Batch
    Go to                               ${PLONEURL}/batches
    Click Link                          Add
    Input Text                          title                   First Batch
    Select from dropdown                Client                  Happy
    Input Text                          description             Nothing to see here...
    Input Text                          WorksOrderID            woid1
    Input Text                          LabelAlcohol            15%
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
    sleep    2
    Log in                              test_labmanager         test_labmanager
    sleep    2
    Go to                               ${PLONEURL}/bika_setup/bika_sampletypes
    Click link                          Red Wine
    Click link                          Wine
    ### Set values
    select from dropdown                WineType                Red        1
    Input text                          Vintage                 2002
    select from dropdown                Cultivar                Cabernet Savignon        1
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
    Should be equal                     ${value}                2002
    ${value} =                          Get Value               Cultivar
    Should be equal                     ${value}                Cabernet Savignon
    ${value} =                          Get Value               Region
    Should be equal                     ${value}                North
    ${value} =                          Get Value               LabelAlcohol
    Should be equal                     ${value}                15.0
    Xpath Should Match X Times          //div[@class='reference_multi_item']//img[@class='deletebtn']    2


*** Keywords ***

Start browser
    Open browser         http://localhost:55001/plone/
    Set selenium speed   0
