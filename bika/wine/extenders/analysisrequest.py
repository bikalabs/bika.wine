from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser.analysisrequest import WidgetVisibility as _WV
from bika.lims.fields import *
from bika.lims.browser.widgets import ReferenceWidget
from bika.lims.interfaces import IAnalysisRequest
from Products.Archetypes.references import HoldingReference
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        schematas['default'] = default
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

# this is done in bika.lims
# class WidgetVisibility(_WV):
#     def __call__(self):
#         ret = _WV.__call__(self)
#         workflow = getToolByName(self.context, 'portal_workflow')
#         state = workflow.getInfoFor(self.context, 'review_state')
#         index_of_batch_field = ret['header_table']['visible'].index('Batch')+1
#         ret['header_table']['visible'].insert(index_of_batch_field, 'SubGroup')
#         if 'Batch' in ret['view']['visible']:
#             index_of_batch_field = ret['view']['visible'].index('Batch')+1
#             ret['view']['visible'].insert(index_of_batch_field, 'SubGroup')
#         elif 'Batch' in ret['edit']['visible']:
#             index_of_batch_field = ret['edit']['visible'].index('Batch')+1
#             ret['edit']['visible'].insert(index_of_batch_field, 'SubGroup')
#         return ret

