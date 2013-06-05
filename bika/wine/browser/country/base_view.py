from bika.lims import bikaMessageFactory as _b
from bika.lims.browser.bika_listing import BikaListingView
from bika.wine import bikaMessageFactory as _
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.layout.globals.interfaces import IViewView
from zope.interface.declarations import implements


class CountryRegionsView(BikaListingView):
    implements(IFolderContentsView, IViewView)

    def __init__(self, context, request):
        super(CountryRegionsView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        path = "/".join(self.context.getPhysicalPath())
        self.contentFilter = {'portal_type': 'Region',
                              'sort_on': 'sortable_title',
                              'path': {'query': path, 'level': 0}
                              }
        self.context_actions = {
            _('Add Region'): {
                'url': 'createObject?type_name=Region',
                'icon': '++resource++bika.lims.images/add.png'
            }
        }
        self.icon = self.portal_url + \
            "/++resource++bika.lims.images/region.png"
        self.title = self.context.Title()
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25

        self.columns = {
            'Title': {'title': _('Region'),
                      'index': 'sortable_title'},
        }

        self.review_states = [
            {'id': 'default',
             'title': _b('Active'),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id': 'deactivate'}, ],
             'columns': ['Title']},
            {'id': 'inactive',
             'title': _b('Inactive'),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id': 'activate'}, ],
             'columns': ['Title']},
            {'id': 'all',
             'title': _b('All'),
             'contentFilter': {},
             'columns': ['Title']},
        ]

        return super(CountryRegionsView, self).__init__(context, request)

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if 'obj' not in items[x]:
                continue
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                (items[x]['url'], items[x]['Title'])

        return items
