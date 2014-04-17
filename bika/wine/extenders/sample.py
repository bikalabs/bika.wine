from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.sample import WidgetVisibility as _WV
from bika.lims.fields import *
from bika.lims.browser.widgets import DateTimeWidget as bikaDateTimeWidget
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
                label=_("Best Before Date"),
                visible={'view': 'visible', 'edit': 'visible', 'header_table': 'visible'},
                modes=('view', 'edit')
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        if 'BestBeforeDate' in default:
            default.remove('BestBeforeDate')
        default.insert(default.index('SamplingDate'), 'BestBeforeDate')
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


class WidgetVisibility(_WV):

    def __call__(self):
        ret = _WV.__call__(self)

        pos = ret['header_table']['visible'].index('SamplingDate') + 1
        ret['header_table']['visible'].insert(pos, 'BestBeforeDate')
        pos = ret['view']['visible'].index('SamplingDate') + 1
        ret['view']['visible'].insert(pos, 'BestBeforeDate')
        # pos = ret['edit']['visible'].index('SamplingDate')+1
        # ret['edit']['visible'].insert(pos, 'BestBeforeDate')
        return ret
