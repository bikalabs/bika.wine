""" Bika setup handlers. """

from bika.wine.permissions import AddCountry
from bika.wine.permissions import AddRegion
from bika.wine.permissions import AddStorageCondition
from bika.wine.permissions import AddSubGroup
from bika.wine.permissions import AddTransportCondition
from bika.wine.permissions import AddWineType
from Products.CMFCore.utils import getToolByName


class Empty:
    pass


def setupWineVarious(context):
    """ Setup Bika site structure """

    if context.readDataFile('bika.wine.txt') is None:
        return
    portal = context.getSite()

    bika_setup = portal._getOb('bika_setup')
    for obj_id in ('bika_regions',
                   'bika_winetypes',
                   'bika_storageconditions',
                   'bika_transportconditions',
                   'bika_subgroups',):
            obj = bika_setup._getOb(obj_id)
            obj.unmarkCreationFlag()
            obj.reindexObject()
    # Plone's jQuery gets clobbered when jsregistry is loaded.
    setup = portal.portal_setup
    setup.runImportStepFromProfile(
        'profile-plone.app.jquery:default', 'jsregistry')
    setup.runImportStepFromProfile(
        'profile-plone.app.jquerytools:default', 'jsregistry')


def setupWinePermissions(context):
    """ Set up some suggested role to permission mappings.
    New types and anything that differs from bika.lims gets specified here.
    These lines completely overwrite those in bika.lims - Changes common to
    both packages should be made in both places!
    """

    if context.readDataFile('bika.wine.txt') is None:
        return
    portal = context.getSite()

    # Root permissions
    mp = portal.manage_permission
    mp(AddCountry, ['Manager', 'LabManager', 'LabClerk'], 0)
    mp(AddRegion, ['Manager', 'LabManager', 'LabClerk'], 0)
    mp(AddSubGroup, ['Manager', 'LabManager', 'LabClerk'], 0)
    mp(AddWineType, ['Manager', 'LabManager', 'LabClerk'], 0)
    mp(AddTransportCondition, ['Manager', 'LabManager', 'LabClerk'], 0)
    mp(AddStorageCondition, ['Manager', 'LabManager', 'LabClerk'], 0)


def setupWineCatalogs(context):
    if context.readDataFile('bika.wine.txt') is None:
        return
    portal = context.getSite()

    def addIndex(cat, *args):
        try:
            cat.addIndex(*args)
        except:
            pass

    def addColumn(cat, col):
        try:
            cat.addColumn(col)
        except:
            pass

    # modify bika_setup_catalog
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('Country',
                         ['portal_catalog', 'bika_setup_catalog', ])
    at.setCatalogsByType('Region',
                         ['portal_catalog', 'bika_setup_catalog', ])
    at.setCatalogsByType('SubGroup',
                         ['portal_catalog', 'bika_setup_catalog', ])
    at.setCatalogsByType('WineType',
                         ['portal_catalog', 'bika_setup_catalog', ])
    at.setCatalogsByType('TransportCondition',
                         ['portal_catalog', 'bika_setup_catalog', ])
    at.setCatalogsByType('StorageCondition',
                         ['portal_catalog', 'bika_setup_catalog', ])


def setupWineTestContent(context):
    """Setup custom content"""

    pass
