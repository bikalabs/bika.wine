from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.browser.widgets import DecimalWidget as bikaDecimalWidget
from bika.lims.fields import *
from bika.lims.interfaces import IBatch
from Products.Archetypes.public import *
from zope.component import adapts
from zope.interface import implements


class BatchSchemaExtender(object):
    adapts(IBatch)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtStringField(
            'WorksOrderID',
            required=True,
            widget=StringWidget(
                label=_('Works Order ID'),
                visible = {'view':'visible',
                           'edit': 'visible'}
            ),
        ),
        ExtStringField(
            'BlendNumber',
            required=False,
            widget=StringWidget(
                label=_('Blend Number'),
                visible = {'view':'visible',
                           'edit': 'visible'}
            ),
        ),
        ExtFloatField(
            'LabelAlcohol',
            required=False,
            validators=('percentvalidator'),
            widget=bikaDecimalWidget(
                label=_('Label Alcohol'),
                unit='%',
                visible = {'view':'visible',
                           'edit': 'visible'}
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        to_insert = [{'name': 'WorksOrderID', 'after': 'description'},
                     {'name': 'BlendNumber', 'after': 'description'},
                     {'name': 'LabelAlcohol', 'after': 'description'}]
        for field in to_insert:
            name = field['name']
            if name in default:
                default.remove(name)
            default.insert(default.index(field['after'])+1, name)
        return schematas

    def getFields(self):
        return self.fields


class BatchSchemaModifier(object):
    adapts(IBatch)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['ClientBatchID'].widget.visible = False
        return schema
