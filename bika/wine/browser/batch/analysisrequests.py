from bika.lims.browser.batch.analysisrequests import AnalysisRequestsView
from bika.wine.browser.analysisrequestsfolder.base_view import AnalysisRequestsView as _ARV


# _ARV adds wine specific columns
class AnalysisRequestsView(AnalysisRequestsView, _ARV):
    pass
