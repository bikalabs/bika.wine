from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from bika.lims.content.bikaschema import BikaSchema
from bika.wine.interfaces import ICultivar
from bika.wine.config import PROJECTNAME
from zope.interface import implements
from bika.wine import bikaMessageFactory as _

schema = BikaSchema.copy() + Schema((
    StringField(
        'Code',
        required=0,
        mode="rw",
        widget=StringWidget(
            label=_("Cultivar Code"),
            description=_("Code to quickly identify the cultivar"),
            visible={'edit': 'visible',
                     'view': 'visible'},
        ),
    ),
))
schema.moveField('Code', before='title')
schema['description'].widget.visible = True
schema['description'].schemata = 'default'


class Cultivar(BaseContent):
    implements(ICultivar)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation

        renameAfterCreation(self)


registerType(Cultivar, PROJECTNAME)
