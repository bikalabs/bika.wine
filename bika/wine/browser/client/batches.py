from bika.lims.browser.client import ClientBatchesView
from bika.wine.browser.batchfolder.base_view import BatchFolderContentsView


class BatchesView(BatchFolderContentsView, ClientBatchesView):

    def contentsMethod(self, contentFilter={}):
        return super(BatchesView, self).contentsMethod(contentFilter)
