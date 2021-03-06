from bika.lims.interfaces import IBatchFolder
from bika.lims.permissions import *
from bika.wine.permissions import *
from bika.lims.vocabularies import CatalogVocabulary
from bika.lims.interfaces import IDisplayListVocabulary
from zope.interface import implements
from zope.component import adapts


class ClientContactVocabularyFactory(CatalogVocabulary):
    implements(IDisplayListVocabulary)
    adapts(IBatchFolder)

    contentFilter = {
        'portal_type': 'Contact',
    }
