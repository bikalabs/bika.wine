from bika.lims.browser import BrowserView
from Products.ATContentTypes.utils import dt2DT

import calendar
import datetime
import datetime
import json
import plone.protect


class Alerts(BrowserView):

    """If the current user has Sampler role, then we want to display an
    alert whenever there are 'sample_due' ARs on which SamplingDate < now."""

    def __call__(self):
        try:
            plone.protect.CheckAuthenticator(self.request)
        except:
            return json.dumps({'error': 'Form authenticator is invalid'})

        member = self.portal_membership.getAuthenticatedMember()
        if not member.has_role('Sampler'):
            return json.dumps({})

        query = {'query': dt2DT(datetime.datetime.now()), 'range': 'max'}

        ars = self.bika_catalog(
            portal_type="AnalysisRequest",
            review_state="sample_due",
            getSamplingDate=query,
        )

        ret = []
        for ar in ars:
            ar = ar.getObject()
            sample = ar.getSample()
            if not hasattr(sample, 'future_dated'):
                continue
            batch_title = ar.getBatch().Title() if ar.getBatch() else ''
            ret.append({
                'UID': ar.UID(),
                'Title': "<a href='{0}'>{1}</a>".format(
                    ar.absolute_url(), ar.Title()),
                'Description': "Works Order ID: {0}".format(batch_title)
                               if batch_title else ''}
            )

        return json.dumps(ret)


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day)
