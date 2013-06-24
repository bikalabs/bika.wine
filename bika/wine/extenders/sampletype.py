from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims.fields import *
from bika.lims.browser.widgets.referencewidget import ReferenceWidget \
    as bikaReferenceWidget
from bika.lims.browser.widgets import DecimalWidget as bikaDecimalWidget
from bika.lims.interfaces import ISampleType
from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from zope.component import adapts
from zope.interface import implements


class SampleTypeSchemaExtender(object):
    adapts(ISampleType)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtStringField(
            'Vintage',
            required=False,
            widget=StringWidget(
                label=_('Vintage'),
            ),
        ),
        ExtReferenceField(
            'WineType',
            required=0,
            allowed_types=('WineType'),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeWineType',
            format='select',
            widget=bikaReferenceWidget(
                label=_('Wine type'),
                render_own_label=False,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'visible'},
                catalog_name='bika_setup_catalog',
                base_query={'inactive_state': 'active'},
                showOn=True,
            ),
        ),
        ExtStringField(
            'Varietal',
            required=False,
            widget=StringWidget(
                label=_('Varietal'),
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
        ExtReferenceField(
            'Region',
            required=0,
            allowed_types = ('Region',),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeRegion',
            format='select',
            widget=bikaReferenceWidget(
                label=_('Region'),
                render_own_label=False,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'visible'},
                catalog_name='bika_setup_catalog',
                base_query={'inactive_state': 'active'},
                showOn=True,
                ui_item='Name',
                colModel=[
                    {'columnName': 'Name',
                     'width': '100', 'label': _('Title'), 'align': 'left'},
                    {'columnName': 'UID', 'hidden': True},
                ],
            ),
        ),
        ExtReferenceField(
            'TransportConditions',
            required=0,
            multiValued=True,
            allowed_types = ('TransportCondition',),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeTransportConditions',
            widget=MultiSelectionWidget(
                label=_("Transport conditions"),
                format="checkbox",
            )
        ),
        ExtReferenceField(
            'StorageConditions',
            required=0,
            multiValued=True,
            allowed_types = ('StorageCondition',),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeStorageConditions',
            widget=MultiSelectionWidget(
                label=_("Storage conditions"),
                format="checkbox",
            )
        ),
        ExtStringField(
            'ShelfLifeType',
            required=False,
            widget=StringWidget(
                label=_('Shelf life type'),
                description=_('Shelf life text to be printed on COA'),
            ),
        ),
        ExtStringField(
            'ShelfLife',
            required=False,
            widget=StringWidget(
                label=_('Shelf life'),
                description=_('Shelf life in months'),
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        # default.remove('...')
        # default.insert(default.index('Field'), 'NewField')
        schematas['default'] = default
        schematas['wine'] = [
            'WineType',
            'Vintage',
            'Varietal',
            'Region',
            'LabelAlcohol',
            'TransportConditions',
            'StorageConditions',
            'ShelfLifeType',
            'ShelfLife']
        return schematas

    def getFields(self):
        return self.fields


class SampleTypeSchemaModifier(object):
    adapts(ISampleType)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        toremove = []
        for field in toremove:
            schema[field].required = False
            schema[field].widget.visible = False
        schema['title'].required = True
        schema['title'].visible = True

        return schema
