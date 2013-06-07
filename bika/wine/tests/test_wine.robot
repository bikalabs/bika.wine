*** Settings ***

Library  Selenium2Library  timeout=10  implicit_wait=5

Suite Setup  Start browser
#Suite Teardown  Close All Browsers

*** Test Cases ***

Test AR new changed and removed fields
    Log in         test_labmanager  test_labmanager
    ## Add Batch
    Go to          http://localhost:55001/plone/batches
    Click Link     Add
    Input Text     title           First Batch
    Input Text     description     Nothing to see here...
    Input Text     WorksOrderID    woid1
    Input Text     LabelAlcohol    15%
    Click element  BatchDate
    Click Link     1
    Click Button   Save
    ## Add Requests in Batch
    Select from list   col_count  2
    click Link         Add new
    ### Check that field defaults were filled correctly
    ${batch_name} =    Get value         ar_0_Batch
    Should be equal    ${batch_name}     First Batch        Batch should be "First Batch" in this batch's context
    ${batch_name} =    Get value         ar_1_Batch
    Should be equal    ${batch_name}     First Batch        Batch should be "First Batch" in this batch's context
    ### Add a new client
    Go to              http://localhost:55001/plone/clients
    Click link         Add
    Input Text         Name              Second Client
    Input Text         ClientID          SecondClient
    Click Button       Save
    Wait until page contains             Changes saved.
    Go to              http://localhost:55001/plone/clients
    Click Link         Second Client
    Click Link         Contacts
    Click Link         Add
    Input Text         Firstname         Andrew
    Input Text         Surname           Dobbs
    Click Button       Save
    ### Add Requests in Client
    Click Link         Second Client
    Click Link         Add
    ### Check that field defaults were filled correctly
    ${batch_name} =    Get value         ar_0_Batch
    Should be equal    ${batch_name}     \               Batch should be empty in Client context
    ${batch_name} =    Get value         ar_1_Batch
    Should be equal    ${batch_name}     \
    ${client_name} =   Get value         ar_0_Client
    Should be equal    ${client_name}    Second Client   Client should be "Second Client" in this client's context
    ${client_name} =   Get value         ar_1_Client
    Should be equal    ${client_name}    Second Client

Test SampleType fields
    Go to                  http://localhost:55001/plone/bika_setup/bika_sampletypes
    ### SampleType Translated to Products
    Click link             Red Wine
    Click link             Wine
    ### Set values
    Input text             WineType                  Red Wine
    Select first option in dropdown
    Input text             Vintage                   a_vintage
    Input text             Varietal                  a_varietal
    Input text             Region                    north-west
    Select first option in dropdown
    Input Text             LabelAlcohol              15%
    Select checkbox        TransportConditions_1
    Select checkbox        StorageConditions_1
    Input text             ShelfLifeType             shelflife_type
    Input text             ShelfLife                 3
    Click button           Save
    Page should contain    Changes saved
    ### Check values saved correctly
    Click link             Wine
    ${value} =             Get Value    WineType
    Should be equal        ${value}     Red Wine
    ${value} =             Get Value    Vintage
    Should be equal        ${value}     a_vintage
    ${value} =             Get Value    Varietal
    Should be equal        ${value}     a_varietal
    ${value} =             Get Value    Region
    Should Contain         ${value}     North-West
    ${value} =             Get Value    LabelAlcohol
    Should be equal        ${value}     15
    Checkbox should be selected      TransportConditions_1
    Checkbox should be selected      StorageConditions_1
    Checkbox should not be selected  StorageConditions_2



*** Keywords ***

Start browser
    Open browser         http://localhost:55001/plone/
    Set selenium speed   0

Log in
    [Arguments]  ${userid}  ${password}

    Go to  http://localhost:55001/plone/login_form
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain button  Log in
    Input text  __ac_name  ${userid}
    Input text  __ac_password  ${password}
    Click Button  Log in

Select First Option in Dropdown
    sleep  0.5
    Click Element  xpath=//div[contains(@class,'cg-DivItem')]
