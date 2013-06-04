from bika.wine.permissions import *
from bika.lims.browser import BrowserView
from bika.lims.permissions import *
from bika.lims.utils import to_utf8 as _c
from Products.CMFCore.utils import getToolByName

import json
import plone.protect


class getARInfo(BrowserView):

    def __init__(self, context, request):
        super(getARInfo, self).__init__(context, request)

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)
        uc = getToolByName(self.context, 'uid_catalog')
        ar_uid = _c(self.request.get('ar_uid', ''))
        column = _c(self.request.get('column', '0'))

        if not ar_uid:
            return {}

        ar = uc(UID=ar_uid)
        if not ar:
            return {}
        ar = ar[0].getObject()

        batch = ar.getBatch()
        client = ar.getClient()
        sampletype = ar.getSampleType()
        categories = []
        services = {}

        for analysis in ar.getAnalyses(full_objects=True):
            service = analysis.getService()
            category = service.getCategory()
            cat_uid = category.UID()
            if cat_uid not in categories:
                categories.append(cat_uid)
            if cat_uid not in services:
                services[cat_uid] = []
            services[cat_uid].append(service.UID())

        ret = {
            'column': column,  # js callback needs to know where the data goes
            'Batch': batch.Title() if batch else '',
            'Batch_uid': batch.UID() if batch else '',
            'Client': client.Title() if client else '',
            'Client_uid': client.UID() if client else '',
            'SampleType': sampletype.Title() if sampletype else '',
            'SampleType_uid': sampletype.UID() if sampletype else '',
            'categories': categories,
            'services': services,
        }

        return json.dumps(ret)
