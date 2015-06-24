import json
from zope import schema
from zope.i18n import translate

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeGrid


class DefaultField(BuilderBase):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IField)

    def __call__(self):
        di = dict(dataIndex=self.field.getName(),
                  text=translate(self.field.title,
                                 context=self.recipe.request)
                  )
        return json.dumps(di, indent=' ' * 4)


class DateField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IDate)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(xtype='datecolumn',
                       dateFormat='Y-m-d H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class TimeField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.ITime)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(xtype='timecolumn',
                       dateFormat='H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class FloatField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IFloat)

    def __call__(self):
        di = json.loads(super(FloatField, self).__call__())
        di.update(dict(xtype='numbercolumn'))
        return json.dumps(di, indent=' ' * 4)
