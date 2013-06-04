from AccessControl import ClassSecurityInfo
from bika.wine.config import PROJECTNAME
from bika.wine.interfaces import IRegion
from bika.lims.content.bikaschema import BikaSchema
from bika.lims.fields import *
from Products.Archetypes.public import *
from zope.interface import implements

schema = BikaSchema.copy() + Schema((
))
schema['description'].widget.visible = True
schema['description'].schemata = 'default'


class Region(BaseContent):
    implements(IRegion)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)

registerType(Region, PROJECTNAME)
