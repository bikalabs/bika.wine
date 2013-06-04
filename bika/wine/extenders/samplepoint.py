from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import *
from bika.lims.interfaces import ISamplePoint
from Products.Archetypes.public import *
from zope.component import adapts
from zope.interface import implements


class SamplePointSchemaExtender(object):
    adapts(ISamplePoint)
    implements(IOrderableSchemaExtender)

    fields = [
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class SamplePointSchemaModifier(object):
    adapts(ISamplePoint)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        toremove = ['Composite']
        for field in toremove:
            schema[field].required = False
            schema[field].widget.visible = False
        schema['title'].required = True
        schema['title'].visible = True

        return schema
