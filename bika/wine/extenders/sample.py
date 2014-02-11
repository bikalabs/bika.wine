from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import *
from bika.lims.interfaces import ISample
from Products.Archetypes.public import *
from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.utils import dt2DT
from datetime import timedelta


class SampleSchemaExtender(object):
    adapts(ISample)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtDateTimeField(
            'BestBeforeDate',
            widget=ComputedWidget(
                visible=False,
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getBestBeforeDate(self):
        bb = ''
        sampletype = self.getSampleType()
        DateSampled = self.getDateSampled()
        months = sampletype.Schema().getField('ShelfLife').get(sampletype)
        if DateSampled and months:
            datesampled = DT2dt(DateSampled)
            try:
                months = int(months)
                bb = datesampled + timedelta(months=months)
                bb = dt2DT(bb)
            except ValueError:
                bb = ''
        else:
            bb = ''
        return bb

    def getOrder(self, schematas):

        default = schematas['default']
        if 'BestBeforeDate' in default:
            default.remove('BestBeforeDate')
        default.insert(default.index('title'), 'BestBeforeDate')
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
