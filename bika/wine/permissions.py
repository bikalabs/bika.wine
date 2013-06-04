"""All permissions are defined here.
They are also defined in permissions.zcml.
The two files must be kept in sync.

"""

# Add Permissions:
AddCountry = 'BIKA: Add Country'
AddRegion = 'BIKA: Add Region'
AddSubGroup = 'BIKA: Add Sub-group'
AddWineType = 'BIKA: Add Wine type'
AddTransportCondition = 'BIKA: Add Transport condition'
AddStorageCondition = 'BIKA: Add Storage condition'

# Add Permissions for specific types, if required
ADD_CONTENT_PERMISSIONS = {
    'Country': AddCountry,
    'Region': AddRegion,
    'WineType': AddWineType,
    'TransportCondition': AddTransportCondition,
    'StorageCondition': AddStorageCondition,
}
