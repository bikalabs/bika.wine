from bika.wine import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims import PloneMessageFactory as _p
from bika.lims.browser.analysisrequest import AnalysisRequestAddView
from bika.lims.browser.bika_listing import WorkflowAction
from bika.lims.subscribers import doActionFor
import plone.protect


class BatchWorkflowAction(WorkflowAction):

    def __call__(self):
        form = self.request.form
        plone.protect.CheckAuthenticator(form)
        action, came_from = WorkflowAction._get_form_workflow_action(self)

        if action == 'submit':

            objects = WorkflowAction._get_selected_items(self)
            if not objects:
                message = self.context.translate(
                    _b("No analyses have been selected"))
                self.context.plone_utils.addPortalMessage(message, 'info')
                self.destination_url = self.context.absolute_url() + \
                    "/batchbook"
                self.request.response.redirect(self.destination_url)
                return

            for ar_uid, ar in objects.items():
                for analysis in ar.getAnalyses(full_objects=True):
                    kw = analysis.getKeyword()
                    values = form.get(kw)
                    analysis.setResult(values[0][ar_uid])
                    if values[0][ar_uid]:
                        doActionFor(analysis, 'submit')

            message = self.context.translate(_p("Changes saved."))
            self.context.plone_utils.addPortalMessage(message, 'info')
            self.request.response.redirect(self.request.get('URL'))
            return

        else:

            WorkflowAction.__call__(self)
