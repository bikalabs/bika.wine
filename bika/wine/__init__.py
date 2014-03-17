# import this to create messages in the bika domain.
from zope.i18nmessageid import MessageFactory
bikaMessageFactory = MessageFactory('bika.wine')

import logging
logger = logging.getLogger('bika.wine')

from bika.lims.validators import *
from bika.lims.config import *
from bika.lims.permissions import *
from bika.wine.config import *
from bika.wine.permissions import *

from AccessControl import allow_module
from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore.utils import ContentInit

allow_module('AccessControl')
allow_module('bika.lims')
allow_module('bika.lims.permissions')
allow_module('bika.lims.utils')
allow_module('bika.wine')
allow_module('bika.wine.permissions')
allow_module('bika.wine.utils')
allow_module('json')
allow_module('pdb')
allow_module('zope.i18n.locales')


def initialize(context):
    ""

    from content.country import Country
    from content.region import Region
    from controlpanel.bika_cultivars import Cultivars
    from content.cultivar import Cultivar
    from controlpanel.bika_regions import Regions
    from controlpanel.bika_winetypes import WineTypes
    from content.winetype import WineType
    from controlpanel.bika_transportconditions import TransportConditions
    from content.transportcondition import TransportCondition
    from controlpanel.bika_storageconditions import StorageConditions
    from content.storagecondition import StorageCondition

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (config.PROJECTNAME, atype.portal_type)
        perm = ADD_CONTENT_PERMISSIONS.get(
            atype.portal_type, ADD_CONTENT_PERMISSION)
        ContentInit(kind,
                    content_types=(atype,),
                    permission = perm,
                    extra_constructors = (constructor,),
                    fti = ftis,
                    ).initialize(context)
