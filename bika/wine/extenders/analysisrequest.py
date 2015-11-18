from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.fields import *
from bika.lims.browser.widgets import DateTimeWidget as bikaDateTimeWidget
from bika.lims.browser.widgets import ReferenceWidget as bikaReferenceWidget
from bika.lims.interfaces import IAnalysisRequest
from bika.wine.extenders.sample import BestBeforeDateField
from zope.component import adapts
from zope.interface import implements


class VintageField(ExtStringField):
    """A computed field which sets and gets a value from Sample
    """

    def get(self, instance):
        sample = instance.getSample()
        if sample:
            return sample.Schema()['Vintage'].get(sample)

    def set(self, instance, value):
        sample = instance.getSample()
        if sample and value:
            sample.Schema()['Vintage'].set(sample, value)


class CultivarField(ExtReferenceField):
    """A computed field which sets and gets a value from Sample
    """

    def get(self, instance):
        sample = instance.getSample()
        if sample:
            return sample.Schema()['Cultivar'].get(sample)

    def set(self, instance, value):
        sample = instance.getSample()
        if sample and value:
            sample.Schema()['Cultivar'].set(sample, value)


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
        # This is included here but refers to the sample
        BestBeforeDateField(
            'BestBeforeDate',
            widget=bikaDateTimeWidget(
                label="Best Before Date",
                visible={'view': 'visible',
                         'edit': 'visible'},
                modes=('view', 'edit')
            ),
        ),
        VintageField(
            'Vintage',
            required=False,
            widget=StringWidget(
                label="Vintage",
                render_own_label=True,
                size=20,
                visible={
                    'edit': 'visible',
                    'view': 'visible',
                    'add': 'edit',
                    'secondary': 'disabled',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible',
                                          'edit': 'visible',
                                          'add': 'edit'},
                    'to_be_sampled': {'view': 'visible',
                                      'edit': 'invisible'},
                    'sampled': {'view': 'visible',
                                'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible',
                                        'edit': 'invisible'},
                    'sample_due': {'view': 'visible',
                                   'edit': 'invisible'},
                    'sample_received': {'view': 'visible',
                                        'edit': 'invisible'},
                    'attachment_due': {'view': 'visible',
                                       'edit': 'invisible'},
                    'to_be_verified': {'view': 'visible',
                                       'edit': 'invisible'},
                    'verified': {'view': 'visible',
                                 'edit': 'invisible'},
                    'published': {'view': 'visible',
                                  'edit': 'invisible'},
                    'invalid': {'view': 'visible',
                                'edit': 'invisible'},
                },
            ),
        ),
        CultivarField(
            'Cultivar',
            required=0,
            allowed_types=['Cultivar'],
            relationship='SampleTypeCultivar',
            format='select',
            widget=bikaReferenceWidget(
                label="Cultivar",
                render_own_label=True,
                size=20,
                catalog_name='bika_setup_catalog',
                base_query={'inactive_state': 'active'},
                showOn=True,
                visible={
                    'edit': 'visible',
                    'view': 'visible',
                    'add': 'edit',
                    'secondary': 'disabled',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible',
                                          'edit': 'visible',
                                          'add': 'edit'},
                    'to_be_sampled': {'view': 'visible',
                                      'edit': 'invisible'},
                    'sampled': {'view': 'visible',
                                'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible',
                                        'edit': 'invisible'},
                    'sample_due': {'view': 'visible',
                                   'edit': 'invisible'},
                    'sample_received': {'view': 'visible',
                                        'edit': 'invisible'},
                    'attachment_due': {'view': 'visible',
                                       'edit': 'invisible'},
                    'to_be_verified': {'view': 'visible',
                                       'edit': 'invisible'},
                    'verified': {'view': 'visible',
                                 'edit': 'invisible'},
                    'published': {'view': 'visible',
                                  'edit': 'invisible'},
                    'invalid': {'view': 'visible',
                                'edit': 'invisible'},
                },
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        # After SamplingDate
        if 'BestBeforeDate' in default:
            default.remove('BestBeforeDate')
        default.insert(default.index('SamplingDate'), 'BestBeforeDate')
        # After SampleType
        pos = schematas['default'].index('SampleType')
        schematas['default'].insert(pos, 'Vintage')
        schematas['default'].insert(pos, 'Cultivar')
        return schematas

    def getFields(self):
        return self.fields


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Add timepicker to SamplingDate
        schema['SamplingDate'].widget.show_time = True

        return schema
