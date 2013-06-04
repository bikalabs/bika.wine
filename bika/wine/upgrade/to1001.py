from Acquisition import aq_inner
from Acquisition import aq_parent
from bika.lims.permissions import *


def upgrade(tool):
    """
    """
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup

    setup.runImportStepFromProfile('profile-bika.wine:default', 'typeinfo')
    setup.runImportStepFromProfile('profile-bika.wine:default', 'workflow')

    # Add Regions folder at bika_setup/bika_regions
    bikasetup = portal['bika_setup']
    typestool.constructContent(type_name="Regions",
                               container=bikasetup,
                               id='bika_regions',
                               title='Regions')
    obj = bikasetup['bika_regions']
    obj.unmarkCreationFlag()
    obj.reindexObject()
    return True

    setup.runImportStepFromProfile('profile-bika.wine:default', 'controlpanel')
