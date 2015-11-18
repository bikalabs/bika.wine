from bika.lims.browser.analysisrequest import AnalysisRequestsView as _ARV
from bika.wine import bikaMessageFactory as _


class AnalysisRequestsView(_ARV):

    def __init__(self, context, request):
        super(AnalysisRequestsView, self).__init__(context, request)
        self.columns.update({
            'WorksOrderID': {'title': _('Works Order ID')},
            'BlendNumber': {'title': _('Blend Number')},
            'Cultivar': {'title': _('Cultivar')},
            'Vintage': {'title': _('Vintage')},
        })

        new_states = []
        for state in self.review_states:
            pos = state['columns'].index('BatchID') + 1
            state['columns'].insert(pos, 'BlendNumber')
            state['columns'].insert(pos, 'WorksOrderID')
            state['columns'].insert(pos, 'Vintage')
            state['columns'].insert(pos, 'Cultivar')
            new_states.append(state)
        self.review_states = new_states

    def folderitems(self):
        items = super(AnalysisRequestsView, self).folderitems()
        for x, item in enumerate(items):
            if not 'obj' in item:
                continue
            obj = items[x]['obj']

            val = obj.Schema().getField('Vintage').get(obj)
            items[x]['Vintage'] = val

            val = obj.Schema().getField('Cultivar').get(obj)
            items[x]['Cultivar'] = val.Title() if val else ''

            batch = obj.Schema().getField('Batch').get(obj)
            if batch:

                val = batch.Schema().getField('WorksOrderID').get(batch)
                items[x]['WorksOrderID'] = val
                items[x]['replace']['WorksOrderID'] = "<a href='%s'>%s</a>" % \
                    (batch.absolute_url(), val)

                val = batch.Schema().getField('BlendNumber').get(batch)
                items[x]['BlendNumber'] = val

            else:
                items[x]['WorksOrderID'] = ''
                items[x]['BlendNumber'] = ''
        return items
