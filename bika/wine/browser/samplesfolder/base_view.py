from bika.lims.browser.sample import SamplesView as _SV
from bika.wine import bikaMessageFactory as _


class SamplesView(_SV):

    def __init__(self, context, request):
        super(SamplesView, self).__init__(context, request)
        self.columns.update({
            'Cultivar': {'title': _('Cultivar')},
            'Vintage': {'title': _('Vintage')},

        })

        new_states = []
        for state in self.review_states:
            pos = state['columns'].index('Requests') + 1
            state['columns'].insert(pos, 'Vintage')
            state['columns'].insert(pos, 'Cultivar')
            new_states.append(state)
        self.review_states = new_states

    def folderitems(self):
        items = super(SamplesView, self).folderitems()
        for x, item in enumerate(items):
            if not 'obj' in item:
                continue
            obj = items[x]['obj']

            val = obj.Schema().getField('Vintage').get(obj)
            items[x]['Vintage'] = val

            val = obj.Schema().getField('Cultivar').get(obj)
            items[x]['Cultivar'] = val.Title() if val else ''

        return items
