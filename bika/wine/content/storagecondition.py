from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from bika.lims.content.bikaschema import BikaSchema
from bika.wine.interfaces import IStorageCondition
from bika.wine.config import PROJECTNAME
from zope.interface import implements

schema = BikaSchema.copy() + Schema((
))
schema['description'].widget.visible = True
schema['description'].schemata = 'default'


class StorageCondition(BaseContent):
    implements(IStorageCondition)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)

registerType(StorageCondition, PROJECTNAME)
