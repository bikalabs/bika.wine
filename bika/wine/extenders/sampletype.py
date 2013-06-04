from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims.fields import *
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
            allowed_types=('Wine type'),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeWineType',
            format='select',
            widget=ReferenceWidget(
                label=_('Wine type'),
                size=12,
                render_own_label=True,
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
        ExtStringField(
            'LabelAlcohol',
            required=False,
            widget=StringWidget(
                label=_('Label Alcohol'),
            ),
        ),
        ExtReferenceField(
            'Country',
            required=0,
            allowed_types = ('Country',),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeCountry',
            format='select',
            widget=ReferenceWidget(
                label=_('Country'),
                size=12,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'visible'},
                catalog_name='bika_setup_catalog',
                base_query={'inactive_state': 'active'},
                showOn=True,
            ),
        ),
        ExtReferenceField(
            'Region',
            required=0,
            allowed_types = ('Region',),
            referenceClass = HoldingReference,
            relationship = 'SampleTypeRegion',
            format='select',
            widget=ReferenceWidget(
                label=_('Region'),
                size=12,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'visible'},
                catalog_name='bika_setup_catalog',
                base_query={'inactive_state': 'active'},
                showOn=True,
            ),
        ),
        ExtReferenceField(
            'TransportConditions',
            required=0,
            allowed_types = ('TransportConditions',),
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
            allowed_types = ('StorageConditions',),
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
            'Country',
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
