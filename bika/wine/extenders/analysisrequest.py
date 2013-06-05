from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.wine import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser.analysisrequest import WidgetVisibility as _WV
from bika.lims.fields import *
from bika.lims.browser.widgets import ReferenceWidget
from bika.lims.interfaces import IAnalysisRequest
from Products.Archetypes.references import HoldingReference
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtReferenceField(
            'SubGroup',
            required=False,
            allowed_types=('SubGroup',),
            referenceClass = HoldingReference,
            relationship = 'AnalysisRequestSubGroup',
            widget=ReferenceWidget(
                label=_('Sub-group'),
                size=12,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'visible'},
                catalog_name='bika_setup_catalog',
                colModel=[
                    {'columnName': 'Title', 'width': '30',
                     'label': _b('Title'), 'align': 'left'},
                    {'columnName': 'Description', 'width': '70',
                     'label': _b('Description'), 'align': 'left'},
                    {'columnName': 'SortKey', 'hidden': True},
                    {'columnName': 'UID', 'hidden': True},
                ],
                base_query={'inactive_state': 'active'},
                sidx='SortKey',
                sord='asc',
                showOn=True,
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        # Insert SubGroup field after Batch
        if 'SubGroup' in default:
            default.remove('SubGroup')
        default.insert(default.index('Batch') + 1, 'SubGroup')
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


class WidgetVisibility(_WV):

    def __call__(self):
        ret = _WV.__call__(self)
        # if self.context.aq_parent.portal_type == 'Client':
        #     ret['add']['visible'].remove('Client')
        #     ret['add']['hidden'].append('Client')
        return ret
