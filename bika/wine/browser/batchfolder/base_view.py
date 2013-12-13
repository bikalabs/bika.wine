from bika.wine import bikaMessageFactory as _
from bika.lims.browser.batchfolder import BatchFolderContentsView as _BFCV
from bika.lims import bikaMessageFactory as _b
from plone.app.content.browser.interfaces import IFolderContentsView
from zope.interface import implements


class BatchFolderContentsView(_BFCV):

    implements(IFolderContentsView)

    def __init__(self, context, request):
        super(BatchFolderContentsView, self).__init__(context, request)

        self.columns = {
            'BatchID': {'title': _('Batch ID')},
            'Title': {'title': _b('Title')},
            'WorksOrderID': {'title': _('Works Order ID')},
            'BlendNumber': {'title': _('Blend Name')},
            'BatchDate': {'title': _b('Date')},
            'Description': {'title': _b('Description')},
            'state_title': {'title': _b('State'), 'sortable': False},
        }

        self.review_states = [  # leave these titles and ids alone
            {'id': 'default',
             'title': _b('All'),
             'contentFilter': {},
             'columns': ['BatchID',
                         'Title',
                         'BlendNumber',
                         'WorksOrderID',
                         'Description',
                         'BatchDate',
                         'state_title', ]
             },
            {'id': 'open',  # in bika.lims, this is 'default'.
             'contentFilter': {'cancellation_state': 'active',
                               'review_state': ['open',
                                                'received',
                                                'to_be_verified',
                                                'verified']},
             'title': _b('Open'),
             'columns': ['BatchID',
                         'Title',
                         'BlendNumber',
                         'WorksOrderID',
                         'Description',
                         'BatchDate',
                         'state_title', ]
             },
            {'id': 'closed',
             'contentFilter': {'review_state': 'closed'},
             'title': _b('Closed'),
             'columns': ['BatchID',
                         'Title',
                         'BlendNumber',
                         'WorksOrderID',
                         'Description',
                         'BatchDate',
                         'state_title', ]
             },
            {'id': 'cancelled',
             'title': _b('Cancelled'),
             'contentFilter': {'cancellation_state': 'cancelled'},
             'columns': ['BatchID',
                         'Title',
                         'BlendNumber',
                         'WorksOrderID',
                         'Description',
                         'BatchDate',
                         'state_title', ]
             },
        ]

    def folderitems(self):
        self.filter_indexes = None

        items = super(BatchFolderContentsView, self).folderitems()
        for x in range(len(items)):
            if 'obj' not in items[x]:
                continue
            obj = items[x]['obj']

            items[x]['replace']['Title'] = \
                "<a href='%s/analysisrequests'>%s</a>" % (items[x]['url'], obj.Title())

            woid = obj.Schema().getField('WorksOrderID').get(obj)
            items[x]['WorksOrderID'] = woid
            items[x]['replace']['WorksOrderID'] = \
                "<a href='%s'>%s</a>" % (items[x]['url'], woid)

            bn = obj.Schema().getField('BlendNumber').get(obj)
            items[x]['BlendNumber'] = bn
            items[x]['replace']['BlendNumber'] = \
                "<a href='%s'>%s</a>" % (items[x]['url'], bn)

            date = obj.Schema().getField('BatchDate').get(obj)
            if callable(date):
                date = date()
            items[x]['BatchDate'] = date
            items[x]['replace']['BatchDate'] = self.ulocalized_time(date)

        return items
