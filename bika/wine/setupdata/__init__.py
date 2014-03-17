from bika.lims.exportimport.dataimport import SetupDataSetList as SDL
from bika.lims.exportimport.setupdata import WorksheetImporter
from bika.lims.idserver import renameAfterCreation
from bika.lims.interfaces import ISetupDataSetList
from bika.lims.utils import tmpID
from zope.interface import implements


class SetupDataSetList(SDL):

    implements(ISetupDataSetList)

    def __call__(self):
        return SDL.__call__(self, projectname="bika.wine")


class Storage_Conditions(WorksheetImporter):

    def Import(self):
        folder = self.context.bika_setup.bika_storageconditions
        for row in self.get_rows(3):
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('StorageCondition', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class Transport_Conditions(WorksheetImporter):

    def Import(self):
        folder = self.context.bika_setup.bika_transportconditions
        for row in self.get_rows(3):
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('TransportCondition', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class Wine_Types(WorksheetImporter):

    def Import(self):
        folder = self.context.bika_setup.bika_winetypes
        for row in self.get_rows(3):
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('WineType', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)

class Cultivars(WorksheetImporter):

    def Import(self):
        folder = self.context.bika_setup.bika_cultivars
        for row in self.get_rows(3):
            if 'title' in row and row['title']:
                _id = folder.invokeFactory('Cultivar', id=tmpID())
                obj = folder[_id]
                obj.edit(title=row['title'],
                         description=row['description'])
                obj.unmarkCreationFlag()
                renameAfterCreation(obj)


class Regions(WorksheetImporter):

    def Import(self):
        folder = self.context.bika_setup.bika_regions
        created = {}
        for row in self.get_rows(3):
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
