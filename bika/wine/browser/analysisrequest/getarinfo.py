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

        batch = ar.getBatch()
        client = ar.getClient()
        contact = ar.getContact()
        # cccontacts = ar.getCCContact()
        ccemails = ar.getCCEmails()
        sampletype = ar.getSampleType()
        samplepoint = ar.getSamplePoint()
        subgroup = ar.Schema()['SubGroup'].get(ar)
        template = ar.getTemplate()
        profile = ar.getProfile()

        ret = {
            'column': column,  # js callback needs to know where the data goes
            'Batch': batch.Title() if batch else '',
            'Batch_uid': batch.UID() if batch else '',
            'Client': client.Title() if client else '',
            'Client_uid': client.UID() if client else '',
            'Contact': contact.getFullname() if contact else '',
            'Contact_uid': contact.UID() if contact else '',
            # 'CCContact': ", ".join([cc.getFullname() for cc in cccontact]) if cccontact else '',
            # 'CCContact_uid': ", ".join([cc.UID() for cc in cccontact]) if cccontact else '',
            'CCEmails': ccemails,
            'SampleType': sampletype.Title() if sampletype else '',
            'SampleType_uid': sampletype.UID() if sampletype else '',
            'SamplePoint': samplepoint.Title() if samplepoint else '',
            'SamplePoint_uid': samplepoint.UID() if samplepoint else '',
            'SubGroup': subgroup.Title() if subgroup else '',
            'SubGroup_uid': subgroup.UID() if subgroup else '',
            'Template': template.Title() if template else '',
            'Template_uid': template.UID() if template else '',
            'Profile': profile.Title() if profile else '',
            'Profile_uid': profile.UID() if profile else '',
            'ClientOrderNumber': ar.getClientOrderNumber(),
            'ClientReference': ar.getSample().getClientReference(),
            'ClientSampleID': ar.getSample().getClientSampleID(),

            'categories': categories,
            'services': services,
        }

        return json.dumps(ret)
