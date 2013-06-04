from bika.lims.browser.client import ClientAnalysisRequestsView as _CARV
from bika.wine.browser.analysisrequestsfolder.base_view import \
    AnalysisRequestsView as _ARV


class AnalysisRequestsView(_ARV, _CARV):
    """bika.wine AR view, with the Client specific view stuff from bika.lims
    """
