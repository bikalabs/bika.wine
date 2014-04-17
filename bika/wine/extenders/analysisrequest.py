from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.analysisrequest import WidgetVisibility as _WV
from bika.lims.fields import *
from bika.lims.browser.widgets import DateTimeWidget as bikaDateTimeWidget
from bika.lims.interfaces import IAnalysisRequest
from bika.wine.extenders.sample import BestBeforeDateField
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
        # This is included here but refers to the sample
        BestBeforeDateField(
            'BestBeforeDate',
            widget=bikaDateTimeWidget(
                label=_("Best Before Date"),
                visible={'view': 'visible', 'edit': 'visible'},
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


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        toremove = ['AdHoc', 'Composite', 'InvoiceExclude']
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
