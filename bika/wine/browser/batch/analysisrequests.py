from bika.lims.browser.batch import BatchAnalysisRequestsView
from bika.wine.browser.analysisrequestsfolder.base_view import AnalysisRequestsView as _ARV
from bika.wine import bikaMessageFactory as _

# _ARV adds wine specific columns
class AnalysisRequestsView(BatchAnalysisRequestsView, _ARV):
    pass
