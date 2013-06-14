from bika.lims.vocabularies import CatalogVocabulary


class BatchContactVocabularyFactory(CatalogVocabulary):

    def __call__(self):
        return super(BatchContactVocabularyFactory, self).__call__(
            portal_type='Contact'
        )
