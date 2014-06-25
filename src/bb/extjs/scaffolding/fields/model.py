from zope import schema

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeModel


class ModelBuilderBase(BuilderBase):
    ext.baseclass()
    
    def base(self, overrides):
        b = dict(name = self.field.getName(),
                 useNull = not self.field.required)
        b.update(overrides)
        return b


class StringField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IField)
    def __call__(self):
        return self.base(dict(type='string'))


class DateField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IDate)
    def __call__(self):
        return self.base(dict(type='date',
                              dateFormat='Y-m-d H:i:s.u'))


class IntField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IInt)
    def __call__(self):
        return self.base(dict(type='int'))

class IdField(IntField):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IId)
