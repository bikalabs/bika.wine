from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims.fields import *
from bika.lims.browser.widgets import DateTimeWidget as bikaDateTimeWidget
from bika.lims.browser.widgets import ReferenceWidget as bikaReferenceWidget
from bika.lims.interfaces import ISample
from bika.wine.utils import add_months
from Products.Archetypes.public import *
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.utils import dt2DT
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements


class BestBeforeDateField(ExtComputedField):
    """Field to calculate BestBeforeDate of a sample.  This is done using
    the "ShelfLife" field of the SampleType, added to either the DateSampled
    or the SamplingDate.
    """

    def getDefault(self, instance):
        pc = getToolByName(instance, 'portal_catalog')
        proxies = pc(portal_type='Client', sort_on='created')
        if proxies:
            return proxies[0].getObject()

    def get(self, instance, **kwargs):
        bb = ''
        sample = instance.getSample() \
            if instance.portal_type == 'AnalysisRequest' else instance
        if not sample:
            # portal_factory ARs have no sample.
            return ''
        sampletype = sample.getSampleType()
        FromDate = sample.getDateSampled()
        if not FromDate:
            FromDate = sample.getSamplingDate()
        months = sampletype.Schema().getField('ShelfLife').get(sampletype)
        if FromDate and months:
            FromDate = DT2dt(FromDate)
            try:
                months = int(months)
                bb = add_months(FromDate, months)
                bb = dt2DT(bb)
            except ValueError:
                bb = ''
        else:
            bb = ''
        return bb

    def getRaw(self, instance, **kwargs):
        bb = ''
        sample = instance.getSample() \
            if instance.portal_type == 'AnalysisRequest' else instance
        if not sample:
            # portal_factory ARs have no sample.
            return ''
        sampletype = sample.getSampleType()
        FromDate = sample.getDateSampled()
        if not FromDate:
            FromDate = sample.getSamplingDate()
        months = sampletype.Schema().getField('ShelfLife').get(sampletype)
        if FromDate and months:
            FromDate = DT2dt(FromDate)
            try:
                months = int(months)
                bb = add_months(FromDate, months)
                bb = dt2DT(bb)
            except ValueError:
                bb = ''
        else:
            bb = ''
        return bb


class SampleSchemaExtender(object):
    adapts(ISample)
    implements(IOrderableSchemaExtender)

    fields = [
        BestBeforeDateField(
            'BestBeforeDate',
            widget=bikaDateTimeWidget(
                label="Best Before Date",
                visible={'view': 'visible',
                         'edit': 'visible',
                         'header_table': 'visible'},
                modes=('view', 'edit')
            ),
        ),
        ExtStringField(
            'Vintage',
            required=False,
            widget=StringWidget(
                label="Vintage",
                render_own_label=True,
                size=20,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible',
                                               'edit': 'visible',
                                               'add': 'edit'},
                         'to_be_sampled': {'view': 'visible',
                                           'edit': 'visible'},
                         'sampled': {'view': 'visible',
                                     'edit': 'visible'},
                         'to_be_preserved': {'view': 'visible',
                                             'edit': 'visible'},
                         'sample_due': {'view': 'visible',
                                        'edit': 'visible'},
                         'sample_received': {'view': 'visible',
                                             'edit': 'visible'},
                         'published': {'view': 'visible',
                                       'edit': 'invisible'},
                         'invalid': {'view': 'visible',
                                     'edit': 'invisible'},
                         },
            ),
        ),
        ExtReferenceField(
            'Cultivar',
            required=0,
            allowed_types=('Cultivar'),
            relationship='SampleTypeCultivar',
            format='select',
            widget=bikaReferenceWidget(
                label="Cultivar",
                render_own_label=True,
                size=20,
                catalog_name='bika_setup_catalog',
                base_query={'inactive_state': 'active'},
                showOn=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible',
                                               'edit': 'visible',
                                               'add': 'edit'},
                         'to_be_sampled': {'view': 'visible',
                                           'edit': 'visible'},
                         'sampled': {'view': 'visible',
                                     'edit': 'visible'},
                         'to_be_preserved': {'view': 'visible',
                                             'edit': 'visible'},
                         'sample_due': {'view': 'visible',
                                        'edit': 'visible'},
                         'sample_received': {'view': 'visible',
                                             'edit': 'visible'},
                         'published': {'view': 'visible',
                                       'edit': 'invisible'},
                         'invalid': {'view': 'visible',
                                     'edit': 'invisible'},
                         },
            ),
        ),
        ExtStringField(
            'Tank',
            widget=StringWidget(
                label=_("Tank"),
                description=_("Tank identifier"),
                visible={'edit': 'visible',
                         'view': 'visible',
                         'header_table': 'visible',
                         'sample_registered': {'view': 'visible',
                                               'edit': 'visible',
                                               'add': 'edit'},
                         'to_be_sampled': {'view': 'visible',
                                           'edit': 'visible'},
                         'sampled': {'view': 'visible',
                                     'edit': 'visible'},
                         'to_be_preserved': {'view': 'visible',
                                             'edit': 'visible'},
                         'sample_due': {'view': 'visible',
                                        'edit': 'visible'},
                         'sample_received': {'view': 'visible',
                                             'edit': 'visible'},
                         'published': {'view': 'visible',
                                       'edit': 'invisible'},
                         'invalid': {'view': 'visible',
                                     'edit': 'invisible'},
                         },
                render_own_label=True,
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        # after SamplingDate
        if 'BestBeforeDate' in default:
            default.remove('BestBeforeDate')
        default.insert(default.index('SamplingDate'), 'BestBeforeDate')
        # after SampleID
        pos = default.index('SampleID')
        default.insert(pos, 'Vintage')
        default.insert(pos, 'Cultivar')
        default.insert(pos, 'Tank')
        return schematas

    def getFields(self):
        return self.fields


class SampleSchemaModifier(object):
    adapts(ISample)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        toremove = ['AdHoc',
                    'Composite']
        for field in toremove:
            schema[field].required = False
            schema[field].widget.visible = False

        # Add timepicker to SamplingDate
        schema['SamplingDate'].widget.show_time = True

        return schema
