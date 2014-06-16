from zope import schema

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.fields import column
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeEditGrid



class DefaultField(BuilderBase):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IField)

    def __call__(self):
        return dict(dataIndex=self.field.getName(),
                    text=self.field.title,
                    field=dict(xtype='textfield'))


class DateField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IDate)

    def __call__(self):
        di = super(DateField, self).__call__()
        di.update(dict(dict(field=dict(xtype='datefield')),
                       dateFormat='Y-m-d H:i:s.u'))
        return di


class FloatField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IFloat)

    def __call__(self):
        di = super(IntField, self).__call__()
        di.update(dict(field=dict(xtype='numberfield')))
        return di


class IdField(column.DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IId)
