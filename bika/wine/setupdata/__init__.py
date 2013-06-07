from bika.lims.exportimport.dataimport import SetupDataSetList as SDL
from bika.lims.idserver import renameAfterCreation
from bika.lims.interfaces import ISetupDataImporter
from bika.lims.interfaces import ISetupDataSetList
from bika.lims.utils import tmpID
from bika.wine import logger
from zope.interface import implements


class SetupDataSetList(SDL):

    implements(ISetupDataSetList)

    def __call__(self):
        return SDL.__call__(self, projectname="bika.wine")


class SubGroups:

    """Import Sub-groups.
    Columns: title, description, SortKey
    """

    implements(ISetupDataImporter)

    def __init__(self, context):
        self.context = context

    def __call__(self, lsd, wb):
        ws = wb.get_sheet_by_name("Sub Groups")
        if not ws:
            logger.info("No SubGroups defined.")
            return
        logger.info("Loading SubGroups...")
        folder = lsd.context.bika_setup.bika_subgroups
        rows = lsd.get_rows(ws, 3)
        for row in rows:
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('SubGroup', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'],
                         SortKey=row['SortKey'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class StorageConditions:

    """Import Storage conditions.
    Columns: title, description
    """

    implements(ISetupDataImporter)

    def __init__(self, context):
        self.context = context

    def __call__(self, lsd, wb):
        ws = wb.get_sheet_by_name("Storage Conditions")
        if not ws:
            logger.info("No Storage conditions defined.")
            return
        logger.info("Loading Storage conditions...")
        folder = lsd.context.bika_setup.bika_storageconditions
        rows = lsd.get_rows(ws, 3)
        for row in rows:
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('StorageCondition', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class TransportConditions:

    """Import Transport conditions.
    Columns: title, description
    """

    implements(ISetupDataImporter)

    def __init__(self, context):
        self.context = context

    def __call__(self, lsd, wb):
        ws = wb.get_sheet_by_name("Transport Conditions")
        if not ws:
            logger.info("No Transport conditions defined.")
            return
        logger.info("Loading Transport conditions...")
        folder = lsd.context.bika_setup.bika_transportconditions
        rows = lsd.get_rows(ws, 3)
        for row in rows:
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('TransportCondition', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class WineTypes:

    """Import Wine types.
    Columns: title, description
    """

    implements(ISetupDataImporter)

    def __init__(self, context):
        self.context = context

    def __call__(self, lsd, wb):
        ws = wb.get_sheet_by_name("Wine Types")
        if not ws:
            logger.info("No Wine types defined.")
            return
        logger.info("Loading Wine types...")
        folder = lsd.context.bika_setup.bika_winetypes
        rows = lsd.get_rows(ws, 3)
        for row in rows:
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('WineType', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class Regions:

    """Import Country and Region values.
    Columns: Country, Region
    """

    implements(ISetupDataImporter)

    def __init__(self, context):
        self.context = context

    def __call__(self, lsd, wb):
        ws = wb.get_sheet_by_name("Regions")
        if not ws:
            logger.info("No Regions defined.")
            return
        logger.info("Loading Regions...")
        folder = lsd.context.bika_setup.bika_regions
        rows = lsd.get_rows(ws, 3)
        created = {}
        for row in rows:
            country = row.get('Country', None)
            region = row.get('Region', None)
            if country and region:
                if country not in created:
                    _id = folder.invokeFactory('Country', id=tmpID())
                    c_obj = folder[_id]
                    c_obj.edit(title=country)
                    c_obj.unmarkCreationFlag()
                    renameAfterCreation(c_obj)
                    created[country] = {'obj': c_obj}
                else:
                    c_obj = created[country]['obj']
                if region not in created[country]:
                    _id = c_obj.invokeFactory('Region', id=tmpID())
                    r_obj = c_obj[_id]
                    r_obj.edit(title=region)
                    r_obj.unmarkCreationFlag()
                    renameAfterCreation(r_obj)
                    created[country][region] = r_obj
