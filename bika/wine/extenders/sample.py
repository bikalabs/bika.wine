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
        DateSampled = self.getDateSampled()
        if DateSampled:
            datesampled = DT2dt(DateSampled)
            datesampled = datesampled + timedelta(months=2)
            DateSampled = dt2DT(datesampled)
        else:
            DateSampled = None
        return DateSampled

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
