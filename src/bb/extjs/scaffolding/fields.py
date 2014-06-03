from zope import schema

from bb.extjs.core import ext
from bb.extjs.scaffolding.interfaces import IFieldBuilder
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipe



@ext.implementer(IFieldBuilder)
class BuilderBase(ext.MultiAdapter):
    ext.baseclass()
    
    def __init__(self, recipe, field):
        self.recipe = recipe
        self.field = field


class StringField(BuilderBase):
    ext.adapts(IScaffoldingRecipe, schema.interfaces.IField)
    def __call__(self):
        return dict(name=self.field.getName(),
                    type='string')


class DateField(BuilderBase):
    ext.adapts(IScaffoldingRecipe, schema.interfaces.IDate)
    def __call__(self):
        return dict(name=self.field.getName(),
                    type='date',
                    dateFormat='Y-m-d H:i:s.u')


class IntField(BuilderBase):
    ext.adapts(IScaffoldingRecipe, schema.interfaces.IInt)
    def __call__(self):
        return dict(name=self.field.getName(),
                    type='int',
                    useNull=True)