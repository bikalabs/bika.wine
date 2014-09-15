from AccessControl.SecurityInfo import ClassSecurityInfo
from bika.wine import bikaMessageFactory as _
from bika.wine.config import PROJECTNAME
from bika.wine.interfaces import ICultivars
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser.bika_listing import BikaListingView
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolderSchema, ATFolder
from plone.app.layout.globals.interfaces import IViewView
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from zope.interface.declarations import implements


class CultivarsView(BikaListingView):
    implements(IFolderContentsView, IViewView)

    def __init__(self, context, request):
        super(CultivarsView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        self.contentFilter = {'portal_type': 'Cultivar',
                              'sort_on': 'sortable_title'}
        self.context_actions = {
            _b('Add'): {
                'url': 'createObject?type_name=Cultivar',
                'icon': '++resource++bika.lims.images/add.png'
            }
        }
        self.icon = self.portal_url + \
            "/++resource++bika.wine.images/winetype_big.png"
        self.title = self.context.translate(_("Cultivars"))
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25

        self.columns = {
            'Title': {'title': _('Cultivar'),
                      'index': 'sortable_title'},
            'Description': {'title': _b('Description'),
                            'index': 'description',
                            'toggle': True},
        }

        self.review_states = [
            {'id': 'default',
             'title': _b('Active'),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id': 'deactivate'}, ],
             'columns': ['Title', 'Description']},
            {'id': 'inactive',
             'title': _b('Inactive'),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id': 'activate'}, ],
             'columns': ['Title', 'Description']},
            {'id': 'all',
             'title': _b('All'),
             'contentFilter': {},
             'columns': ['Title', 'Description']},
        ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if 'obj' not in items[x]:
                continue
            obj = items[x]['obj']
            items[x]['Description'] = obj.Description()
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                (items[x]['url'], items[x]['Title'])

        return items

schema = ATFolderSchema.copy()


class Cultivars(ATFolder):
    implements(ICultivars)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)
atapi.registerType(Cultivars, PROJECTNAME)
