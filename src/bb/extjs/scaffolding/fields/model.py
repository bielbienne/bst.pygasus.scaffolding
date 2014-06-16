from zope import schema

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeModel



class StringField(BuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IField)
    def __call__(self):
        return dict(name=self.field.getName(),
                    type='string')


class DateField(BuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IDate)
    def __call__(self):
        return dict(name=self.field.getName(),
                    type='date',
                    dateFormat='Y-m-d H:i:s.u')


class IntField(BuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IInt)
    def __call__(self):
        return dict(name=self.field.getName(),
                    type='int',
                    useNull=True)

class IdField(IntField):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IId)
