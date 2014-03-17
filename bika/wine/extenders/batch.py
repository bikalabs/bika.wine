from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.browser.widgets import RecordsWidget as bikaRecordsWidget
from bika.lims.browser.widgets import DecimalWidget as bikaDecimalWidget
from bika.lims.fields import *
from bika.lims.interfaces import IBatch
from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from Products.ATExtensions.ateapi import RecordsField
from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapts
from zope.interface import implements
from plone.indexer import indexer


class InheritedObjectsUIField(ExtensionField, RecordsField):

    """XXX bika.lims.RecordsWidget doesn't cater for multiValued fields
    InheritedObjectsUI is a RecordsField because we want the RecordsWidget,
    but the values are stored in ReferenceField 'InheritedObjects'
    """

    def get(self, instance, **kwargs):
        # Return the formatted contents of InheritedObjects field.
        field = instance.Schema()['InheritedObjects']
        value = field.get(instance)
        return [{'Title': x.Title(),
                 'ObjectID': x.id,
                 'Description': x.Description()} for x in value]

    def getRaw(self, instance, **kwargs):
        # Return the formatted contents of InheritedObjects field.
        field = instance.Schema()['InheritedObjects']
        value = field.get(instance)
        return [{'Title': x.Title(),
                 'ObjectID': x.id,
                 'Description': x.Description()} for x in value]

    def set(self, instance, value, **kwargs):
        _field = instance.Schema().getField('InheritedObjects')
        uids = []
        if value:
            bc = getToolByName(instance, 'bika_catalog')
            ids = [x['ObjectID'] for x in value]
            if ids:
                proxies = bc(id=ids)
                if proxies:
                    uids = [x.UID for x in proxies]
        RecordsField.set(self, instance, value)
        return _field.set(instance, uids)


class BatchSchemaExtender(object):
    adapts(IBatch)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtStringField(
            'WorksOrderID',
            required=True,
            widget=StringWidget(
                label=_('Works Order ID'),
            ),
        ),
        ExtStringField(
            'BlendNumber',
            required=False,
            widget=StringWidget(
                label=_('Blend Number'),
            ),
        ),
        ExtFloatField(
            'LabelAlcohol',
            required=False,
            validators=('percentvalidator'),
            widget=bikaDecimalWidget(
                label=_('Label Alcohol'),
                unit='%',
            ),
        ),
        InheritedObjectsUIField(
            'InheritedObjectsUI',
            required=False,
            type='InheritedObjects',
            subfields=('Title', 'ObjectID', 'Description'),
            subfield_sizes = {'Title': 25,
                              'ObjectID': 25,
                              'Description': 50,
                              },
            subfield_labels = {'Title': _b('Title'),
                               'ObjectID': _('Object ID'),
                               'Description': _b('Description')
                               },
            widget = bikaRecordsWidget(
                label=_("Inherit From"),
                description=_(
                    "Include all analysis requests belonging to the selected objects."),
                innerJoin="<br/>",
                combogrid_options={
                    'Title': {
                        'colModel': [
                            {'columnName': 'Title', 'width': '25',
                             'label': _('Title'), 'align': 'left'},
                            {'columnName': 'ObjectID', 'width': '25',
                             'label': _('Object ID'), 'align': 'left'},
                            {'columnName': 'Description', 'width': '50',
                             'label': _b('Description'), 'align': 'left'},
                            {'columnName': 'UID', 'hidden': True},
                        ],
                        'url': 'getAnalysisContainers',
                        'showOn': True,
                        'width': '600px'
                    },
                    'ObjectID': {
                        'colModel': [
                            {'columnName': 'Title', 'width': '25',
                             'label': _('Title'), 'align': 'left'},
                            {'columnName': 'ObjectID', 'width': '25',
                             'label': _('Object ID'), 'align': 'left'},
                            {'columnName': 'Description', 'width': '50',
                             'label': _b('Description'), 'align': 'left'},
                            {'columnName': 'UID', 'hidden': True},
                        ],
                        'url': 'getAnalysisContainers',
                        'showOn': False,
                        'width': '600px'
                    },
                },
            ),
        ),
        ReferenceField(
            'InheritedObjects',
            required=0,
            multiValued=True,
            allowed_types=('AnalysisRequest'),
            referenceClass = HoldingReference,
            relationship = 'BatchInheritedObjects',
            widget=ReferenceWidget(
                visible=False,
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        to_insert = [{'name': 'WorksOrderID', 'before': 'description'},
                     {'name': 'BlendNumber', 'before': 'description'},
                     {'name': 'LabelAlcohol', 'before': 'description'}]
        for field in to_insert:
            name = field['name']
            if name in default:
                default.remove(name)
            default.insert(default.index(field['before']), name)
        default.append("InheritedObjectsUI")
        default.append("InheritedObjects")
        return schematas

    def getFields(self):
        return self.fields


class BatchSchemaModifier(object):
    adapts(IBatch)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['ClientBatchID'].required = False
        schema['ClientBatchID'].widget.visible = False
        schema['title'].required = True
        schema['title'].widget.visible = True
        return schema





# class WidgetVisibility(_WV):

#     def __call__(self):
#         ret = _WV.__call__(self)
#         if self.context.aq_parent.portal_type == 'Client':
#             ret['add']['visible'].remove('Client')
#             ret['add']['hidden'].append('Client')
#         return ret
